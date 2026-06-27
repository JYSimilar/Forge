#!/usr/bin/env python3
"""Validate Forge multi-agent JSON indexes."""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

VALID_STATUSES = {"planned", "ready", "running", "blocked", "needs_review", "done", "failed"}


@dataclass
class ValidationResult:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def _is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _expect_text(obj: dict[str, Any], key: str, label: str, errors: list[str]) -> None:
    if not _is_text(obj.get(key)):
        errors.append(f"{label}.{key} is required")


def _expect_string_list(obj: dict[str, Any], key: str, label: str, errors: list[str]) -> None:
    value = obj.get(key)
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        errors.append(f"{label}.{key} must be a list of strings")


def _scope(value: str) -> str:
    normalized = value.replace("\\", "/").strip().strip("/")
    for suffix in ("/**", "/*", "*"):
        if normalized.endswith(suffix):
            normalized = normalized[: -len(suffix)].strip("/")
    return normalized or "."


def _scopes_overlap(left: str, right: str) -> bool:
    a = _scope(left)
    b = _scope(right)
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


def _within_any_scope(path: str, scopes: list[str]) -> bool:
    normalized = _scope(path)
    return any(normalized == _scope(scope) or normalized.startswith(_scope(scope) + "/") for scope in scopes)


def _artifact_scopes(payload: dict[str, Any]) -> list[str]:
    artifacts = payload.get("artifacts")
    scopes: list[str] = []

    def collect(value: Any) -> None:
        if isinstance(value, str) and value.strip():
            scopes.append(value)
        elif isinstance(value, list):
            for item in value:
                collect(item)
        elif isinstance(value, dict):
            for item in value.values():
                collect(item)

    collect(artifacts)
    return scopes


def validate_index(payload: Any) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(payload, dict):
        return ValidationResult(["top-level JSON must be an object"], warnings)

    for key in ("schema_version", "task_id", "status"):
        _expect_text(payload, key, "root", errors)
    if payload.get("status") and payload.get("status") not in VALID_STATUSES:
        errors.append(f"root.status must be one of {sorted(VALID_STATUSES)}")

    agents = payload.get("agents")
    tasks = payload.get("tasks")
    write_locks = payload.get("write_locks", [])

    if not isinstance(agents, list) or not agents:
        errors.append("root.agents must be a non-empty list")
        agents = []
    if not isinstance(tasks, list):
        errors.append("root.tasks must be a list")
        tasks = []
    if not isinstance(write_locks, list):
        errors.append("root.write_locks must be a list")
        write_locks = []

    agent_ids: set[str] = set()
    agents_by_id: dict[str, dict[str, Any]] = {}
    allowed_scopes: list[tuple[str, str]] = []
    for index, agent in enumerate(agents):
        label = f"agents[{index}]"
        if not isinstance(agent, dict):
            errors.append(f"{label} must be an object")
            continue
        for key in ("id", "role", "model", "goal", "status"):
            _expect_text(agent, key, label, errors)
        if agent.get("status") and agent.get("status") not in VALID_STATUSES:
            errors.append(f"{label}.status must be one of {sorted(VALID_STATUSES)}")
        agent_id = agent.get("id")
        if _is_text(agent_id):
            if agent_id in agent_ids:
                errors.append(f"{label}.id duplicates agent id {agent_id!r}")
            agent_ids.add(agent_id)
            agents_by_id[agent_id] = agent
        for key in ("allowed_files", "forbidden_files"):
            _expect_string_list(agent, key, label, errors)
        if isinstance(agent.get("allowed_files"), list) and _is_text(agent_id):
            for scope in agent["allowed_files"]:
                if isinstance(scope, str) and scope.strip():
                    allowed_scopes.append((agent_id, scope))
        if isinstance(agent.get("allowed_files"), list) and isinstance(agent.get("forbidden_files"), list):
            for allowed in agent["allowed_files"]:
                for forbidden in agent["forbidden_files"]:
                    if isinstance(allowed, str) and isinstance(forbidden, str) and _scopes_overlap(allowed, forbidden):
                        errors.append(f"{label}.allowed_files conflicts with forbidden_files: {allowed} vs {forbidden}")

    for left_index, (left_agent, left_scope) in enumerate(allowed_scopes):
        for right_agent, right_scope in allowed_scopes[left_index + 1 :]:
            if left_agent != right_agent and _scopes_overlap(left_scope, right_scope):
                errors.append(
                    "overlapping write scope: "
                    f"{left_agent}:{left_scope} conflicts with {right_agent}:{right_scope}"
                )

    task_ids = {task.get("id") for task in tasks if isinstance(task, dict) and _is_text(task.get("id"))}
    shared_artifacts = _artifact_scopes(payload)
    for index, task in enumerate(tasks):
        label = f"tasks[{index}]"
        if not isinstance(task, dict):
            errors.append(f"{label} must be an object")
            continue
        for key in ("id", "title", "assigned_agent", "goal", "status"):
            _expect_text(task, key, label, errors)
        for key in ("input", "output", "dependencies", "acceptance"):
            _expect_string_list(task, key, label, errors)
        if task.get("status") and task.get("status") not in VALID_STATUSES:
            errors.append(f"{label}.status must be one of {sorted(VALID_STATUSES)}")
        assigned = task.get("assigned_agent")
        if _is_text(assigned) and assigned not in agent_ids:
            errors.append(f"{label}.assigned_agent references unknown assigned_agent {assigned!r}")
        dependencies = task.get("dependencies")
        if isinstance(dependencies, list):
            for dependency in dependencies:
                if isinstance(dependency, str) and dependency not in task_ids:
                    errors.append(f"{label}.dependencies references unknown dependency {dependency!r}")
        outputs = task.get("output")
        if _is_text(assigned) and assigned in agents_by_id and isinstance(outputs, list):
            allowed = agents_by_id[assigned].get("allowed_files", [])
            if not isinstance(allowed, list):
                allowed = []
            for output in outputs:
                if not isinstance(output, str):
                    continue
                if not _within_any_scope(output, allowed) and not _within_any_scope(output, shared_artifacts):
                    errors.append(f"{label}.output {output!r} is outside allowed scope for agent {assigned!r}")

    lock_owners: dict[str, str] = {}
    for index, lock in enumerate(write_locks):
        label = f"write_locks[{index}]"
        if not isinstance(lock, dict):
            errors.append(f"{label} must be an object")
            continue
        _expect_text(lock, "path", label, errors)
        _expect_text(lock, "owner", label, errors)
        owner = lock.get("owner")
        path = lock.get("path")
        if _is_text(owner) and owner not in agent_ids:
            errors.append(f"{label}.owner references unknown agent {owner!r}")
        if _is_text(path) and _is_text(owner):
            normalized = _scope(path)
            previous_owner = lock_owners.get(normalized)
            if previous_owner and previous_owner != owner:
                errors.append(f"{label}.path {path!r} is locked by both {previous_owner!r} and {owner!r}")
            lock_owners[normalized] = owner

    if agents and not write_locks:
        warnings.append("write_locks is empty; concurrent writers should be coordinated manually")

    return ValidationResult(errors, warnings)


def run(index_path: str) -> int:
    path = Path(index_path).expanduser()
    if not path.exists() or not path.is_file():
        print(f"Invalid AGENT_INDEX path: {path}", file=sys.stderr)
        return 2
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        return 2

    result = validate_index(payload)
    if result.ok:
        print("Agent index is valid.")
        for warning in result.warnings:
            print(f"Warning: {warning}")
        return 0

    print("Agent index is invalid.", file=sys.stderr)
    for error in result.errors:
        print(f"- {error}", file=sys.stderr)
    for warning in result.warnings:
        print(f"Warning: {warning}", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Forge AGENT_INDEX.json file.")
    parser.add_argument("index", help="Path to AGENT_INDEX.json")
    args = parser.parse_args()
    return run(args.index)


if __name__ == "__main__":
    raise SystemExit(main())
