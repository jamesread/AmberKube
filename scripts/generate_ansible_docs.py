#!/usr/bin/env python3
"""Generate MkDocs pages for each Ansible role."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover - script guard
    raise SystemExit("PyYAML is required. Install it with `pip install pyyaml`.") from exc

TASK_METADATA_KEYS = {
    "name",
    "when",
    "tags",
    "vars",
    "register",
    "changed_when",
    "notify",
    "loop",
    "loop_control",
    "with_items",
    "delegate_to",
    "run_once",
    "environment",
    "become",
    "become_user",
    "block",
    "rescue",
    "always",
}


def slug_to_title(slug: str) -> str:
    parts = slug.replace("_", " ").replace("-", " ").split()
    return " ".join(part.capitalize() for part in parts) if parts else slug


def list_files(role_dir: Path) -> list[str]:
    return [
        str(path.relative_to(role_dir))
        for path in sorted(role_dir.rglob("*"))
        if path.is_file()
    ]


def read_description(role_dir: Path) -> str:
    for candidate in ("README.md", "README"):
        readme = role_dir / candidate
        if not readme.exists():
            continue
        for line in readme.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            return stripped
    return "Role documentation pending."


def parse_tasks(task_file: Path) -> list[dict]:
    if not task_file.exists():
        return []

    documents = yaml.safe_load(task_file.read_text(encoding="utf-8"))
    if not isinstance(documents, list):
        return []

    tasks: list[dict] = []

    def visit(items: Iterable[dict]) -> None:
        for item in items:
            if not isinstance(item, dict):
                continue
            name = item.get("name")
            module = next(
                (
                    key
                    for key in item
                    if key not in TASK_METADATA_KEYS
                    and not key.startswith("with_")
                ),
                None,
            )
            if name:
                tasks.append({"name": name, "module": module})
            block = item.get("block")
            if isinstance(block, list):
                visit(block)
            for keyword in ("rescue", "always"):
                section = item.get(keyword)
                if isinstance(section, list):
                    visit(section)

    visit(documents)
    return tasks


def render_tasks_section(tasks: list[dict]) -> str:
    if not tasks:
        return "## Tasks\n- No tasks discovered.\n\n"

    lines = ["## Tasks"]
    for task in tasks:
        module = f" _({task['module']})_" if task.get("module") else ""
        lines.append(f"- {task['name']}{module}")
    lines.append("")
    return "\n".join(lines)


def render_markdown(role_dir: Path, repo_root: Path) -> str:
    repo_url = f"https://github.com/jamesread/AmberKube/tree/main/{role_dir.relative_to(repo_root).as_posix()}"
    title = slug_to_title(role_dir.name)
    description = read_description(role_dir)
    files = list_files(role_dir)
    files_section = "\n".join(f"- `{relative}`" for relative in files) or "- (no files yet)"

    tasks_file = role_dir / "tasks" / "main.yml"
    if not tasks_file.exists():
        tasks_file = role_dir / "tasks" / "main.yaml"
    tasks_section = render_tasks_section(parse_tasks(tasks_file))

    return (
        f"# {title}\n\n"
        f"- **Role path:** [`{role_dir.relative_to(repo_root)}`]({repo_url})\n"
        f"- **Description:** {description}\n\n"
        f"{tasks_section}"
        f"## Files\n"
        f"{files_section}\n"
    )


def generate_docs(roles_dir: Path, docs_dir: Path) -> None:
    repo_root = roles_dir.parents[2] if len(roles_dir.parents) > 2 else roles_dir.parent
    target_dir = docs_dir / "ansible"
    target_dir.mkdir(parents=True, exist_ok=True)

    role_dirs = [
        path for path in sorted(roles_dir.iterdir()) if path.is_dir() and not path.name.startswith(".")
    ]
    if not role_dirs:
        raise SystemExit(f"No role directories found in {roles_dir}")

    for role_dir in role_dirs:
        markdown = render_markdown(role_dir, repo_root)
        output_file = target_dir / f"{role_dir.name}.md"
        output_file.write_text(markdown, encoding="utf-8")
        print(f"Wrote {output_file}")


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    default_roles = repo_root / "iac" / "ansible" / "roles"
    default_docs = repo_root / "docs" / "source"

    parser = argparse.ArgumentParser(description="Generate MkDocs pages for each Ansible role.")
    parser.add_argument(
        "--roles-dir",
        default=default_roles,
        type=Path,
        help=f"Path to the Ansible roles directory (default: {default_roles})",
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
    generate_docs(args.roles_dir.resolve(), args.docs_dir.resolve())


if __name__ == "__main__":
    main()
