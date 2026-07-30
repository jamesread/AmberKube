#!/usr/bin/env python3
"""Discover Flux HelmReleases, render them with helm template, validate with kubeconform."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
APPS_ROOT = ROOT / "iac" / "kubernetes"
# Skip vendored CRD dumps (gotk-components, etc.)
MAX_MANIFEST_BYTES = 100_000


def load_docs(path: Path) -> list[dict]:
    try:
        docs = list(yaml.safe_load_all(path.read_text()))
    except yaml.YAMLError as exc:
        raise RuntimeError(f"failed to parse {path}: {exc}") from exc
    return [d for d in docs if isinstance(d, dict)]


def app_namespace(app_dir: Path) -> str:
    kust = app_dir / "kustomization.yaml"
    if kust.exists():
        for doc in load_docs(kust):
            ns = doc.get("namespace")
            if ns:
                return ns
    return "default"


def discover_releases() -> list[dict]:
    releases: list[dict] = []
    for app_dir in sorted(APPS_ROOT.glob("*/app")):
        repos: dict[str, str] = {}
        pending: list[tuple[Path, dict]] = []
        for path in sorted(app_dir.glob("*.yaml")):
            if path.stat().st_size > MAX_MANIFEST_BYTES:
                continue
            for doc in load_docs(path):
                kind = doc.get("kind")
                if kind == "HelmRepository":
                    name = doc["metadata"]["name"]
                    repos[name] = doc["spec"]["url"]
                elif kind == "HelmRelease":
                    pending.append((path, doc))

        ns = app_namespace(app_dir)
        for path, doc in pending:
            chart_spec = doc["spec"]["chart"]["spec"]
            source = chart_spec["sourceRef"]["name"]
            if source not in repos:
                raise RuntimeError(f"{path}: HelmRepository {source!r} not found in {app_dir}")

            values_file: Path | None = None
            inline_values = doc["spec"].get("values")
            values_from = doc["spec"].get("valuesFrom") or []
            if values_from:
                # Repo convention: ConfigMap-backed values live in app/values.yaml
                candidate = app_dir / "values.yaml"
                if not candidate.exists():
                    raise RuntimeError(f"{path}: valuesFrom set but {candidate} missing")
                values_file = candidate

            releases.append(
                {
                    "app": app_dir.parent.name,
                    "name": doc["metadata"]["name"],
                    "namespace": ns,
                    "chart": chart_spec["chart"],
                    "version": chart_spec.get("version"),
                    "repo_name": source,
                    "repo_url": repos[source],
                    "values_file": values_file,
                    "inline_values": inline_values,
                    "path": path,
                }
            )
    return releases


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=False, text=True, capture_output=True, **kwargs)


def ensure_repo(repo_name: str, repo_url: str) -> None:
    listed = run(["helm", "repo", "list", "-o", "yaml"])
    if listed.returncode != 0:
        raise RuntimeError(listed.stderr or listed.stdout)
    existing = yaml.safe_load(listed.stdout) or []
    for row in existing:
        if row.get("name") == repo_name:
            if row.get("url") == repo_url:
                return
            raise RuntimeError(
                f"helm repo {repo_name!r} already points at {row.get('url')}, expected {repo_url}"
            )
    added = run(["helm", "repo", "add", repo_name, repo_url])
    if added.returncode != 0:
        raise RuntimeError(added.stderr or added.stdout)


def template_release(release: dict, out_dir: Path) -> Path:
    ensure_repo(release["repo_name"], release["repo_url"])
    update = run(["helm", "repo", "update", release["repo_name"]])
    if update.returncode != 0:
        raise RuntimeError(update.stderr or update.stdout)

    out_path = out_dir / f"{release['app']}-{release['name']}.yaml"
    chart_ref = f"{release['repo_name']}/{release['chart']}"
    cmd = [
        "helm",
        "template",
        release["name"],
        chart_ref,
        "--namespace",
        release["namespace"],
    ]
    if release["version"]:
        cmd.extend(["--version", str(release["version"])])

    with tempfile.TemporaryDirectory(prefix="amberkube-helm-") as tmp:
        tmp_path = Path(tmp)
        if release["values_file"] is not None:
            cmd.extend(["-f", str(release["values_file"])])
        elif release["inline_values"] is not None:
            values_path = tmp_path / "values.yaml"
            values_path.write_text(yaml.safe_dump(release["inline_values"], sort_keys=False))
            cmd.extend(["-f", str(values_path)])

        rendered = run(cmd)
        if rendered.returncode != 0:
            raise RuntimeError(
                f"helm template failed for {release['app']}/{release['name']}:\n"
                f"{rendered.stderr or rendered.stdout}"
            )
        out_path.write_text(rendered.stdout)
    return out_path


def kubeconform_paths(paths: list[Path]) -> None:
    if not paths:
        print("kubeconform: nothing to validate")
        return
    cmd = [
        "kubeconform",
        "-strict",
        "-summary",
        "-skip",
        "CustomResourceDefinition",
        *[str(p) for p in paths],
    ]
    result = run(cmd)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    if result.returncode != 0:
        raise RuntimeError("kubeconform reported validation errors")


def kubeconform_kustomize() -> None:
    failures: list[str] = []
    for app_dir in sorted(APPS_ROOT.glob("*/app")):
        built = run(["kustomize", "build", str(app_dir)])
        if built.returncode != 0:
            failures.append(f"{app_dir}: kustomize build failed:\n{built.stderr or built.stdout}")
            continue
        if not built.stdout.strip():
            print(f"kubeconform kustomize: skip empty {app_dir}")
            continue
        cmd = [
            "kubeconform",
            "-strict",
            "-summary",
            "-ignore-missing-schemas",
            "-",
        ]
        result = subprocess.run(
            cmd,
            input=built.stdout,
            text=True,
            capture_output=True,
            check=False,
        )
        print(f"kubeconform kustomize: {app_dir}")
        sys.stdout.write(result.stdout)
        if result.stderr:
            sys.stderr.write(result.stderr)
        if result.returncode != 0:
            failures.append(f"{app_dir}: kubeconform failed")
    if failures:
        raise RuntimeError("\n".join(failures))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "tmp" / "helm-template",
        help="Directory for rendered Helm manifests",
    )
    parser.add_argument(
        "--skip-kubeconform",
        action="store_true",
        help="Only render HelmReleases; do not run kubeconform",
    )
    parser.add_argument(
        "--kustomize",
        action="store_true",
        help="Also kubeconform kustomize build output for each app",
    )
    args = parser.parse_args()

    releases = discover_releases()
    if not releases:
        print("No HelmReleases discovered", file=sys.stderr)
        return 1

    args.out_dir.mkdir(parents=True, exist_ok=True)
    rendered_paths: list[Path] = []
    for release in releases:
        print(
            f"helm template: {release['app']}/{release['name']} "
            f"({release['repo_name']}/{release['chart']}"
            f"{'@' + release['version'] if release['version'] else ''})"
        )
        rendered_paths.append(template_release(release, args.out_dir))

    if not args.skip_kubeconform:
        print("kubeconform: helm template outputs")
        kubeconform_paths(rendered_paths)
        if args.kustomize:
            kubeconform_kustomize()

    print(f"OK: rendered {len(rendered_paths)} HelmRelease(s)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
