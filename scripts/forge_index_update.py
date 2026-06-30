#!/usr/bin/env python3
"""Safely update Forge dual-index evidence and re-render Markdown."""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    from scripts.dual_index_builder import render_markdown
except ImportError:  # pragma: no cover - used when run directly from scripts/
    from dual_index_builder import render_markdown


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("top-level JSON must be an object")
    return payload


def _atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        tmp_name = handle.name
        handle.write(text)
    os.replace(tmp_name, path)


def _ensure_list(payload: dict[str, Any], key: str) -> list[Any]:
    value = payload.setdefault(key, [])
    if not isinstance(value, list):
        raise ValueError(f"root.{key} must be a list")
    return value


def _ensure_artifacts(payload: dict[str, Any]) -> dict[str, Any]:
    artifacts = payload.setdefault("artifacts", {})
    if not isinstance(artifacts, dict):
        raise ValueError("root.artifacts must be an object")
    return artifacts


def update_payload(
    payload: dict[str, Any],
    status: str | None = None,
    evidence: str | None = None,
    risk: str | None = None,
    artifact: str | None = None,
) -> dict[str, Any]:
    if status:
        payload["status"] = status
        statuses = _ensure_list(payload, "statuses")
        if status not in statuses:
            statuses.append(status)
    if evidence:
        evidence_items = _ensure_list(payload, "evidence")
        evidence_items.append(evidence)
    if risk:
        risk_items = _ensure_list(payload, "risks")
        risk_items.append(risk)
    if artifact:
        artifacts = _ensure_artifacts(payload)
        additional = artifacts.setdefault("additional", [])
        if not isinstance(additional, list):
            raise ValueError("root.artifacts.additional must be a list")
        additional.append(artifact)
    return payload


def _write_payload(index_path: Path, markdown_path: Path | None, payload: dict[str, Any]) -> None:
    _atomic_write_text(index_path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    if markdown_path:
        _atomic_write_text(markdown_path, render_markdown(payload))


def run(
    index_path: str,
    markdown_path: str | None = None,
    status: str | None = None,
    evidence: str | None = None,
    risk: str | None = None,
    artifact: str | None = None,
) -> int:
    path = Path(index_path).expanduser()
    if not path.exists() or not path.is_file():
        print(f"Invalid forge_index.json path: {path}", file=sys.stderr)
        return 2
    try:
        payload = _load_json(path)
        updated = update_payload(payload, status=status, evidence=evidence, risk=risk, artifact=artifact)
        markdown = Path(markdown_path).expanduser() if markdown_path else None
        _write_payload(path, markdown, updated)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"Updated {path}")
    if markdown_path:
        print(f"Rendered {Path(markdown_path).expanduser()}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Safely update Forge forge_index.json and re-render FORGE_INDEX.md.")
    parser.add_argument("index", help="Path to forge_index.json")
    parser.add_argument("--markdown", dest="markdown_path", help="Path to FORGE_INDEX.md to re-render")
    parser.add_argument("--status", help="Optional status to set and append to statuses")
    parser.add_argument("--evidence", help="Optional evidence line to append")
    parser.add_argument("--risk", help="Optional risk line to append")
    parser.add_argument("--artifact", help="Optional artifact path to append under artifacts.additional")
    args = parser.parse_args()
    return run(args.index, args.markdown_path, args.status, args.evidence, args.risk, args.artifact)


if __name__ == "__main__":
    raise SystemExit(main())
