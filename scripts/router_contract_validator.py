#!/usr/bin/env python3
"""Validate and simulate Forge router contracts."""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_ROUTE_FIELDS = {
    "id",
    "name",
    "triggers",
    "minimum_reference",
    "default_output",
    "completion_evidence",
    "handoff",
    "token_mode_default",
}


@dataclass
class ValidationResult:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass
class RouteDecision:
    route_id: str
    score: int
    matched_triggers: list[str]
    token_mode: str
    minimum_reference: str


def _is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _expect_text(obj: dict[str, Any], key: str, label: str, errors: list[str]) -> None:
    if not _is_text(obj.get(key)):
        errors.append(f"{label}.{key} is required")


def _expect_string_list(obj: dict[str, Any], key: str, label: str, errors: list[str]) -> None:
    value = obj.get(key)
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        errors.append(f"{label}.{key} must be a non-empty list of strings")


def _normalize(value: str) -> str:
    return " ".join(value.casefold().strip().split())


def load_contract(contract_path: str | Path) -> dict[str, Any]:
    path = Path(contract_path).expanduser()
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _find_repo_root(start: Path) -> Path:
    current = start if start.is_dir() else start.parent
    for candidate in (current, *current.parents):
        if (candidate / "SKILL.md").exists():
            return candidate
    return current


def _path_exists(base_dir: Path, reference: str) -> bool:
    if reference == "none":
        return True
    return (base_dir / reference).exists()


def validate_contract(payload: Any, base_dir: str | Path | None = None) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    root = Path(base_dir).expanduser() if base_dir is not None else None

    if not isinstance(payload, dict):
        return ValidationResult(["top-level JSON must be an object"], warnings)

    for key in ("schema_version", "mode_default", "fallback_route_id"):
        _expect_text(payload, key, "root", errors)

    routes = payload.get("routes")
    if not isinstance(routes, list) or not routes:
        errors.append("root.routes must be a non-empty list")
        routes = []

    route_ids: set[str] = set()
    for index, route in enumerate(routes):
        label = f"routes[{index}]"
        if not isinstance(route, dict):
            errors.append(f"{label} must be an object")
            continue
        missing = sorted(REQUIRED_ROUTE_FIELDS - set(route))
        for field in missing:
            errors.append(f"{label}.{field} is required")
        for key in ("id", "name", "minimum_reference", "default_output", "handoff", "token_mode_default"):
            if key in route:
                _expect_text(route, key, label, errors)
        minimum_reference = route.get("minimum_reference")
        if root is not None and _is_text(minimum_reference) and not _path_exists(root, minimum_reference):
            errors.append(f"{label}.minimum_reference path does not exist: {minimum_reference}")
        for key in ("triggers", "completion_evidence"):
            if key in route:
                _expect_string_list(route, key, label, errors)
        route_id = route.get("id")
        if _is_text(route_id):
            if route_id in route_ids:
                errors.append(f"{label}.id duplicates route id {route_id!r}")
            route_ids.add(route_id)
        priority = route.get("priority", 0)
        if not isinstance(priority, int):
            errors.append(f"{label}.priority must be an integer when present")
        optional_references = route.get("optional_references", [])
        if optional_references and not all(isinstance(item, str) and item.strip() for item in optional_references):
            errors.append(f"{label}.optional_references must be a list of strings when present")
        if root is not None and isinstance(optional_references, list):
            for reference in optional_references:
                if isinstance(reference, str) and reference.strip() and not _path_exists(root, reference):
                    errors.append(f"{label}.optional_references path does not exist: {reference}")

    fallback = payload.get("fallback_route_id")
    if _is_text(fallback) and fallback not in route_ids:
        errors.append(f"root.fallback_route_id references unknown route {fallback!r}")

    if len(route_ids) < 8:
        warnings.append("router contract has fewer than 8 routes; check whether Forge coverage is too narrow")

    return ValidationResult(errors, warnings)


def simulate_route(payload: dict[str, Any], prompt: str) -> RouteDecision:
    prompt_norm = _normalize(prompt)
    best_route: dict[str, Any] | None = None
    best_score = -1
    best_matches: list[str] = []
    best_priority = -1

    for route in payload.get("routes", []):
        if not isinstance(route, dict):
            continue
        matches: list[str] = []
        score = 0
        for trigger in route.get("triggers", []):
            if not isinstance(trigger, str) or not trigger.strip():
                continue
            trigger_norm = _normalize(trigger)
            if trigger_norm and trigger_norm in prompt_norm:
                matches.append(trigger)
                score += max(1, len(trigger_norm))
        priority = route.get("priority", 0)
        if not isinstance(priority, int):
            priority = 0
        if score > best_score or (score == best_score and priority > best_priority):
            best_route = route
            best_score = score
            best_matches = matches
            best_priority = priority

    if best_route is None or best_score <= 0:
        fallback = payload.get("fallback_route_id")
        for route in payload.get("routes", []):
            if isinstance(route, dict) and route.get("id") == fallback:
                best_route = route
                best_score = 0
                best_matches = []
                break

    if best_route is None:
        return RouteDecision("unknown", 0, [], "", "")

    return RouteDecision(
        route_id=str(best_route.get("id", "unknown")),
        score=max(best_score, 0),
        matched_triggers=best_matches,
        token_mode=str(best_route.get("token_mode_default", "")),
        minimum_reference=str(best_route.get("minimum_reference", "")),
    )


def run(contract_path: str | Path, simulate_prompt: str | None = None) -> int:
    path = Path(contract_path).expanduser()
    if not path.exists() or not path.is_file():
        print(f"Invalid router contract path: {path}", file=sys.stderr)
        return 2
    try:
        payload = load_contract(path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        return 2

    result = validate_contract(payload, base_dir=_find_repo_root(path))
    if not result.ok:
        print("Router contract is invalid.", file=sys.stderr)
        for error in result.errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Router contract is valid.")
    for warning in result.warnings:
        print(f"Warning: {warning}")

    if simulate_prompt:
        decision = simulate_route(payload, simulate_prompt)
        print(json.dumps(decision.__dict__, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and simulate a Forge ROUTER_CONTRACT.json file.")
    parser.add_argument("contract", help="Path to ROUTER_CONTRACT.json")
    parser.add_argument("--simulate", help="Prompt to route through the contract")
    args = parser.parse_args()
    return run(args.contract, args.simulate)


if __name__ == "__main__":
    raise SystemExit(main())
