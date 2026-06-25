#!/usr/bin/env python3
"""Create a lightweight project documentation scaffold."""
from __future__ import annotations

import argparse
from pathlib import Path

FILES = {
    "README.md": "# Project Name\n\n## What is this?\n\n## Quick Start\n\n## Documentation\n\n- QUICKSTART.md\n- CONFIG.md\n- TESTING.md\n- TROUBLESHOOTING.md\n",
    "QUICKSTART.md": "# Quick Start\n\n## Install\n\n## Configure\n\n## Run\n\n## Verify\n",
    "CONFIG.md": "# Configuration\n\n| Name | Description | Example |\n|---|---|---|\n|  |  |  |\n",
    "TESTING.md": "# Testing\n\n## Automated Tests\n\n```bash\n\n```\n\n## Manual Verification\n\n1. \n",
    "TROUBLESHOOTING.md": "# Troubleshooting\n\n| Problem | Possible Cause | Fix |\n|---|---|---|\n|  |  |  |\n",
    "CHANGELOG.md": "# Changelog\n\n## Unreleased\n\n- \n",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create standard project docs such as README, QUICKSTART, CONFIG, TESTING, and TROUBLESHOOTING.",
        epilog="Example: python scripts/new_project_scaffold.py /path/to/project --force",
    )
    parser.add_argument("project", nargs="?", default=".", help="Project directory, defaults to current directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing scaffold files")
    args = parser.parse_args()

    root = Path(args.project).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    created = []
    overwritten = []
    skipped = []
    for name, content in FILES.items():
        path = root / name
        if path.exists() and not args.force:
            skipped.append(name)
            continue
        existed = path.exists()
        path.write_text(content, encoding="utf-8")
        (overwritten if existed else created).append(name)

    print("# Scaffold Result")
    print(f"Project: {root}")
    if created:
        print("Created:")
        for name in created:
            print(f"- {name}")
    if overwritten:
        print("Overwritten:")
        for name in overwritten:
            print(f"- {name}")
    if skipped:
        print("Skipped existing:")
        for name in skipped:
            print(f"- {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
