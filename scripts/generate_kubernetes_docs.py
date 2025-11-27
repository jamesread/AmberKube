#!/usr/bin/env python3
"""Generate MkDocs pages for each infra component."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover - script guard
    raise SystemExit(
        "PyYAML is required. Install it with `pip install pyyaml`."
    ) from exc


def slug_to_title(slug: str) -> str:
    """Convert directory slug to title-friendly text."""
    parts = slug.replace("_", " ").replace("-", " ").split()
    return " ".join(part.capitalize() for part in parts) if parts else slug


def list_files(component_dir: Path) -> list[str]:
    """Return all files inside the component directory relative to it."""
    return [
        str(path.relative_to(component_dir))
        for path in sorted(component_dir.rglob("*"))
        if path.is_file()
    ]


def locate_kustomization(component_dir: Path) -> Path | None:
    """Find the kustomization file if it exists."""
    candidates = [
        component_dir / "kustomization.yaml",
        component_dir / "kustomization.yml",
        component_dir / "Kustomization",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def load_yaml_documents(file_path: Path) -> Iterable[dict]:
    """Yield parsed YAML documents from a file, ignoring empty ones."""
    try:
        with file_path.open("r", encoding="utf-8") as handle:
            for doc in yaml.safe_load_all(handle):
                if isinstance(doc, dict):
                    yield doc
    except FileNotFoundError:
        return


def find_helm_releases(component_dir: Path, repo_root: Path) -> list[dict]:
    """Locate HelmRelease resources referenced via kustomization.yaml."""
    kustomization = locate_kustomization(component_dir)
    if not kustomization:
        return []

    docs = [
        doc
        for doc in yaml.safe_load_all(kustomization.read_text(encoding="utf-8"))
        if isinstance(doc, dict)
    ]
    data = docs[0] if docs else {}
    resources = data.get("resources") or []

    releases: list[dict] = []
    for resource in resources:
        resource_path = (kustomization.parent / resource).resolve()
        if resource_path.is_file():
            paths = [resource_path]
        elif resource_path.is_dir():
            paths = sorted(resource_path.rglob("*.y*ml"))
        else:
            continue

        for path in paths:
            for doc in load_yaml_documents(path):
                if doc.get("kind") != "HelmRelease":
                    continue
                metadata = doc.get("metadata") or {}
                spec = doc.get("spec") or {}
                chart_spec = (((spec.get("chart") or {}).get("spec") or {}))
                try:
                    relative_source = path.relative_to(repo_root)
                except ValueError:
                    relative_source = path
                releases.append(
                    {
                        "name": metadata.get("name", "unknown"),
                        "namespace": metadata.get("namespace", "default"),
                        "chart": chart_spec.get("chart"),
                        "version": chart_spec.get("version"),
                        "source": str(relative_source),
                    }
                )
    return releases


def render_deployment_section(releases: list[dict]) -> str:
    """Format HelmRelease data as markdown."""
    if not releases:
        return (
            "## Deployment Type\n"
            "- Kubernetes manifest (no HelmRelease resources detected).\n\n"
        )

    lines = ["## Deployment Type"]
    for release in releases:
        details = [
            f"name: `{release['name']}`",
            f"namespace: `{release['namespace']}`",
        ]
        if release["chart"]:
            version = f"@{release['version']}" if release["version"] else ""
            details.append(f"chart: `{release['chart']}{version}`")
        details.append(f"source: `{release['source']}`")
        lines.append(f"- HelmRelease ({', '.join(details)})")
    lines.append("")  # blank line at end
    return "\n".join(lines)


def repo_url_for(path: Path, repo_root: Path) -> str:
    relative = path.relative_to(repo_root)
    return f"https://github.com/jamesread/AmberKube/tree/main/{relative.as_posix()}"


def load_metadata(component_dir: Path) -> dict:
    """Read metadata.yaml if present and return a dict."""
    metadata_path = component_dir / "metadata.yaml"
    if not metadata_path.exists():
        return {}
    data = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def render_markdown(component_dir: Path, repo_root: Path) -> str:
    """Build the markdown body for a component directory."""
    title = slug_to_title(component_dir.name)
    metadata = load_metadata(component_dir)
    description = metadata.get("description") or "Add component notes here."
    homepage = metadata.get("homepage")
    repository = metadata.get("repository")
    files = list_files(component_dir)
    files_section = "\n".join(f"- `{relative}`" for relative in files) or "- (no files yet)"
    deployment_section = render_deployment_section(find_helm_releases(component_dir, repo_root))

    links_lines = []
    if homepage:
        links_lines.append(f"- **Homepage:** [{homepage}]({homepage})")
    if repository:
        links_lines.append(f"- **Repository:** [{repository}]({repository})")
    links_section = "\n".join(links_lines)
    if links_section:
        links_section += "\n"

    return (
        f"# {title}\n\n"
        f"- **Component path:** [`{component_dir.relative_to(repo_root)}`]({repo_url_for(component_dir, repo_root)})\n"
        f"- **Description:** _{description}_\n\n"
        f"{links_section}"
        f"{deployment_section}"
        f"## Files\n"
        f"{files_section}\n"
    )


def generate_docs(infra_dir: Path, docs_dir: Path) -> None:
    """Create (or overwrite) documentation pages for infra components."""
    repo_root = infra_dir.parents[1] if len(infra_dir.parents) > 1 else infra_dir.parent
    target_dir = docs_dir / "kubernetes"
    target_dir.mkdir(parents=True, exist_ok=True)

    component_dirs = [
        path for path in sorted(infra_dir.iterdir()) if path.is_dir() and not path.name.startswith(".")
    ]

    if not component_dirs:
        raise SystemExit(f"No component directories found in {infra_dir}")

    for component_dir in component_dirs:
        markdown = render_markdown(component_dir, repo_root)
        output_file = target_dir / f"{component_dir.name}.md"
        output_file.write_text(markdown, encoding="utf-8")
        print(f"Wrote {output_file}")


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    default_infra = repo_root / "iac" / "kubernetes"
    default_docs = repo_root / "docs" / "source"

    parser = argparse.ArgumentParser(
        description="Generate MkDocs pages for each infra component directory."
    )
    parser.add_argument(
        "--infra-dir",
        default=default_infra,
        type=Path,
        help=f"Path to the infra directory (default: {default_infra})",
    )
    parser.add_argument(
        "--docs-dir",
        default=default_docs,
        type=Path,
        help=f"Path to the MkDocs source directory (default: {default_docs})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generate_docs(args.infra_dir.resolve(), args.docs_dir.resolve())


if __name__ == "__main__":
    main()
