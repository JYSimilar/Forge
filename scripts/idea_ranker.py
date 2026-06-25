#!/usr/bin/env python3
"""Rank brainstormed product ideas from a CSV file."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

SCORE_COLUMNS = [
    "user_value",
    "prototype_speed",
    "demo_effect",
    "tech_fit",
    "extensibility",
    "differentiation",
    "engineering_value",
    "risk_control",
]

WEIGHTS = {
    "user_value": 1.3,
    "prototype_speed": 1.1,
    "demo_effect": 1.1,
    "tech_fit": 1.0,
    "extensibility": 1.0,
    "differentiation": 1.0,
    "engineering_value": 1.0,
    "risk_control": 1.2,
}


def to_score(value: str | None) -> float:
    try:
        score = float(value or "")
    except ValueError:
        return 0.0
    return max(0.0, min(5.0, score))


def escape_markdown_cell(value: str) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ").strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rank product ideas from a CSV file. Required column: idea. Optional 0-5 score columns: "
        + ", ".join(SCORE_COLUMNS),
        epilog="Example: python scripts/idea_ranker.py ideas.csv",
    )
    parser.add_argument("csv_file", help="CSV file containing an idea column and optional score columns")
    args = parser.parse_args()

    path = Path(args.csv_file).expanduser().resolve()
    if not path.exists() or not path.is_file():
        print(f"Error: file not found: {path}")
        return 2

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    if not rows or "idea" not in rows[0]:
        print("Error: CSV must contain an 'idea' column.")
        return 2

    ranked = []
    for row in rows:
        total = 0.0
        for col in SCORE_COLUMNS:
            total += to_score(row.get(col)) * WEIGHTS[col]
        ranked.append((total, row.get("idea", ""), row))

    ranked.sort(reverse=True, key=lambda item: item[0])

    print("| Rank | Idea | Weighted Score | Suggestion |")
    print("|---:|---|---:|---|")
    for idx, (total, idea, _) in enumerate(ranked, start=1):
        if idx == 1:
            suggestion = "最推荐先做"
        elif total >= 28:
            suggestion = "可作为备选"
        else:
            suggestion = "不建议现在做"
        print(f"| {idx} | {escape_markdown_cell(idea)} | {total:.1f} | {suggestion} |")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
