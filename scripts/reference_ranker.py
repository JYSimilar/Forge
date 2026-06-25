#!/usr/bin/env python3
"""Rank open-source/product reference candidates from a CSV file."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

POSITIVE_FIELDS = ["fit", "speed", "docs", "maintenance", "license", "compatibility", "extension"]
RISK_FIELD = "risk"

WEIGHTS = {
    "fit": 2.0,
    "speed": 1.2,
    "docs": 1.0,
    "maintenance": 1.2,
    "license": 1.5,
    "compatibility": 1.0,
    "extension": 1.0,
    "risk": -1.5,
}


def num(row: dict[str, str], key: str) -> float:
    raw = (row.get(key) or "").strip()
    if not raw:
        return 0.0
    try:
        value = float(raw)
    except ValueError:
        return 0.0
    return max(0.0, min(5.0, value))


def score(row: dict[str, str]) -> float:
    total = 0.0
    for key in POSITIVE_FIELDS:
        total += num(row, key) * WEIGHTS[key]
    total += num(row, RISK_FIELD) * WEIGHTS[RISK_FIELD]
    return round(total, 2)


def decision(row: dict[str, str], value: float) -> str:
    risk = num(row, RISK_FIELD)
    license_score = num(row, "license")
    fit = num(row, "fit")
    docs = num(row, "docs")
    if license_score <= 1:
        return "learn-only / reject: license unclear or risky"
    if risk >= 4:
        return "learn-only: risk is high"
    if value >= 35 and fit >= 4 and docs >= 3:
        return "strong reference"
    if value >= 28:
        return "usable reference"
    if value >= 20:
        return "minor reference"
    return "reject or keep as weak reference"


def escape(value: str) -> str:
    return str(value).replace("|", "/").replace("\n", " ").strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rank open-source/product references from a CSV file. Expected columns: name,type,fit,speed,docs,maintenance,license,compatibility,extension,risk,notes.",
        epilog="Example: python scripts/reference_ranker.py references.csv",
    )
    parser.add_argument("csv_file", help="CSV file with 0-5 reference scores")
    args = parser.parse_args()

    path = Path(args.csv_file).expanduser().resolve()
    if not path.exists() or not path.is_file():
        print(f"Error: file not found: {path}")
        return 2

    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print("No rows found.")
        return 0

    ranked = []
    for row in rows:
        value = score(row)
        ranked.append((value, row, decision(row, value)))
    ranked.sort(key=lambda item: item[0], reverse=True)

    print("# Reference Ranking\n")
    print("Scores assume 0-5 values. Higher risk lowers the score.\n")
    print("| Rank | Name | Type | Score | Decision | Notes |")
    print("|---:|---|---|---:|---|---|")
    for idx, (value, row, dec) in enumerate(ranked, start=1):
        name = escape(row.get("name", ""))
        typ = escape(row.get("type", ""))
        notes = escape(row.get("notes", ""))
        print(f"| {idx} | {name} | {typ} | {value} | {dec} | {notes} |")

    print("\n## Next Step\n")
    print("Use the top references to decide what to borrow, what to avoid, and what belongs in the MVP.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
