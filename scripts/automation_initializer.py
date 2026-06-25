#!/usr/bin/env python3
"""Create lightweight automation planning files for a project.

Usage:
  python scripts/automation_initializer.py /path/to/project
  python scripts/automation_initializer.py /path/to/project --force
"""
from __future__ import annotations

import argparse
from pathlib import Path

TEMPLATES = {
    "AUTOMATION_PLAN.md": """# Automation Plan\n\n## Goal\n\n## User / Audience\n\n## Deliverable\n\n## Inputs Needed\n\n## Constraints\n\n- Platform:\n- Time:\n- Budget:\n- Tools:\n- Privacy / security:\n- Complexity limit:\n\n## Automation Level\n\n- [ ] Level 0: Plan only\n- [ ] Level 1: Guided steps\n- [ ] Level 2: Prepare assets\n- [ ] Level 3: Safe local execution\n- [ ] Level 4: Confirmation-gated execution\n\n## Options Considered\n\n| Option | Description | Effort | Risk | Best For | Decision |\n|---|---|---|---|---|---|\n| Fastest | | | | | |\n| Stable | | | | | |\n| Low-tech | | | | | |\n| Extensible | | | | | |\n\n## Recommended Path\n\n## Definition of Done\n\n## Stop Conditions\n\n## Action Batches\n\n### Batch 1\n\n- Actions:\n- Expected result:\n- Verification:\n- Needs confirmation:\n\n## Risks\n\n## Next Checkpoint\n""",
    "TASK_QUEUE.md": """# Task Queue\n\n| ID | Task | Stage | Priority | Status | Owner | Verification | Notes |\n|---|---|---|---|---|---|---|\n| T1 | | | High | Pending | | | |\n\n## Status Values\n\n- Pending\n- In Progress\n- Blocked\n- Needs user choice\n- Needs confirmation\n- Done\n- Skipped\n\n## Current Batch\n\n1.\n2.\n3.\n\n## Waiting For User\n\n## Completed This Round\n\n## Next Suggested Batch\n""",
    "OPTION_SET.md": """# Option Set\n\n## Current Decision\n\n## Assumptions\n\n## Options\n\n| Option | What It Does | Pros | Cons | Effort | Risk | Best Fit |\n|---|---|---|---|---|---|---|\n| A | | | | | | |\n| B | | | | | | |\n| C | | | | | | |\n\n## Recommendation\n\n## User Choice\n\n## Rejected Options\n\n## New Constraints\n\n## If None Are Good\n\nPlease clarify which part is wrong: goal, target user, platform, complexity, cost, timeline, tech stack, privacy, output format, or other.\n\n## Revised Constraints\n""",
}


def write_file(path: Path, content: str, force: bool) -> str:
    if path.exists() and not force:
        return f"skip existing: {path.name}"
    path.write_text(content, encoding="utf-8")
    return f"created: {path.name}" if not path.exists() else f"written: {path.name}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize Forge automation planning files.")
    parser.add_argument("project", help="Project directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    if not project.exists():
        print(f"Error: path does not exist: {project}")
        return 2
    if not project.is_dir():
        print(f"Error: path is not a directory: {project}")
        return 2

    for name, content in TEMPLATES.items():
        target = project / name
        existed = target.exists()
        if existed and not args.force:
            print(f"skip existing: {name}")
        else:
            target.write_text(content, encoding="utf-8")
            print(("overwritten" if existed else "created") + f": {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
