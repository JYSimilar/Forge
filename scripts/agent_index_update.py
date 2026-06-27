#!/usr/bin/env python3
"""Safely update Forge AGENT_INDEX.json status fields."""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    from scripts.agent_index_validator import VALID_STATUSES, validate_index
except ImportError:  # pragma: no cover - used when run directly from scripts/
    from agent_index_validator import VALID_STATUSES, validate_index


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("top-level JSON must be an object")
    return payload


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        tmp_name = handle.name
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    os.replace(tmp_name, path)


def _target_list(payload: dict[str, Any], target_type: str) -> list[dict[str, Any]]:
    key = {"agent": "agents", "task": "tasks"}[target_type]
    values = payload.get(key)
    if not isinstance(values, list):
        raise ValueError(f"root.{key} must be a list")
    return [item for item in values if isinstance(item, dict)]


def update_index(
    payload: dict[str, Any],
    target_type: str,
    target_id: str,
    status: str,
    evidence: str | None = None,
    artifact: str | None = None,
) -> dict[str, Any]:
    if target_type not in {"agent", "task"}:
        raise ValueError("target_type must be 'agent' or 'task'")
    if status not in VALID_STATUSES:
        raise ValueError(f"status must be one of {sorted(VALID_STATUSES)}")

    matches = [item for item in _target_list(payload, target_type) if item.get("id") == target_id]
    if not matches:
        raise ValueError(f"{target_type} {target_id!r} was not found")
    target = matches[0]
    target["status"] = status
    if evidence:
        target.setdefault("evidence", [])
        if not isinstance(target["evidence"], list):
            raise ValueError(f"{target_type} {target_id!r} evidence must be a list")
        target["evidence"].append(evidence)
    if artifact:
        target.setdefault("artifacts", [])
        if not isinstance(target["artifacts"], list):
            raise ValueError(f"{target_type} {target_id!r} artifacts must be a list")
        target["artifacts"].append(artifact)
    return payload


def run(
    index_path: str,
    target_type: str,
    target_id: str,
    status: str,
    evidence: str | None = None,
    artifact: str | None = None,
) -> int:
    path = Path(index_path).expanduser()
    if not path.exists() or not path.is_file():
        print(f"Invalid AGENT_INDEX path: {path}", file=sys.stderr)
        return 2
    try:
        payload = _load_json(path)
        updated = update_index(payload, target_type, target_id, status, evidence, artifact)
        result = validate_index(updated)
        if not result.ok:
            print("Refusing to write invalid AGENT_INDEX.", file=sys.stderr)
            for error in result.errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        _atomic_write_json(path, updated)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"Updated {target_type} {target_id} -> {status}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Safely update a Forge AGENT_INDEX.json agent or task status.")
    parser.add_argument("index", help="Path to AGENT_INDEX.json")
    parser.add_argument("--type", choices=["agent", "task"], required=True, dest="target_type")
    parser.add_argument("--id", required=True, dest="target_id", help="Agent id or task id")
    parser.add_argument("--status", choices=sorted(VALID_STATUSES), required=True)
    parser.add_argument("--evidence", help="Optional evidence line to append")
    parser.add_argument("--artifact", help="Optional artifact path to append")
    args = parser.parse_args()
    return run(args.index, args.target_type, args.target_id, args.status, args.evidence, args.artifact)


if __name__ == "__main__":
    raise SystemExit(main())
