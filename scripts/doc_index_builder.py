#!/usr/bin/env python3
"""Build a simple Markdown documentation index."""
from __future__ import annotations

import argparse
from pathlib import Path

IGNORED_PARTS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}


def first_heading(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except OSError:
        pass
    return path.stem


def is_ignored(path: Path) -> bool:
    return any(part in IGNORED_PARTS for part in path.parts)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a Markdown documentation index for a project.",
        epilog="Example: python scripts/doc_index_builder.py /path/to/project > DOC_INDEX.md",
    )
    parser.add_argument("project", nargs="?", default=".", help="Project directory, defaults to current directory")
    args = parser.parse_args()

    root = Path(args.project).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"Error: project path does not exist or is not a directory: {root}")
        return 2

    docs = sorted(p for p in root.rglob("*.md") if not is_ignored(p.relative_to(root)))

    print("# Documentation Index")
    print()
    if not docs:
        print("No Markdown files found.")
        return 0

    for doc in docs:
        rel = doc.relative_to(root)
        print(f"- [{first_heading(doc)}]({rel.as_posix()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
