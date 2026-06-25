#!/usr/bin/env python3
"""Initialize Forge project-state templates in a project directory."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

TEMPLATE_NAMES = [
    "PROJECT_STATE.md",
    "DECISION_LOG.md",
    "RETROSPECTIVE.md",
    "PROJECT_HANDOFF.md",
    "IDEA_BACKLOG.md",
]

FALLBACK_CONTENT = {
    "PROJECT_STATE.md": "# PROJECT_STATE\n\n## 项目目标\n\n## 当前阶段\n\n## 下一步计划\n\n",
    "DECISION_LOG.md": "# Decision Log\n\n| Date | Decision | Options Considered | Why This Option | Trade-offs | Revisit When |\n|---|---|---|---|---|---|\n",
    "RETROSPECTIVE.md": "# Retrospective\n\n## 本轮目标\n\n## 实际完成\n\n## 下一轮计划\n\n",
    "PROJECT_HANDOFF.md": "# Project Handoff\n\n## 项目简介\n\n## 如何运行\n\n## 如何测试\n\n## 已知问题\n\n",
    "IDEA_BACKLOG.md": "# Idea Backlog\n\n| Idea | Why It Was Deferred | Revisit When | Target Version / Stage | Priority | Effort | Risk | Status |\n|---|---|---|---|---|---|---|---|\n",
}


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def template_dir() -> Path:
    return package_root() / "assets" / "templates"


def copy_or_write_template(name: str, target: Path, force: bool) -> str:
    destination = target / name
    if destination.exists() and not force:
        return f"skip   {name} already exists"

    source = template_dir() / name
    if source.exists():
        shutil.copyfile(source, destination)
        return f"write  {name}"

    destination.write_text(FALLBACK_CONTENT[name], encoding="utf-8")
    return f"write  {name} (fallback)"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create Forge project-state templates in a project directory. Existing files are not overwritten unless --force is used."
    )
    parser.add_argument("project", help="Path to the target project directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    target = Path(args.project).expanduser().resolve()
    if not target.exists():
        print(f"ERROR: target path does not exist: {target}", file=sys.stderr)
        return 2
    if not target.is_dir():
        print(f"ERROR: target path is not a directory: {target}", file=sys.stderr)
        return 2

    print(f"Initializing Forge project templates in: {target}")
    for name in TEMPLATE_NAMES:
        print(copy_or_write_template(name, target, args.force))

    print("Done. Suggested next step: fill PROJECT_STATE.md first, then park deferred ideas in IDEA_BACKLOG.md when needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
