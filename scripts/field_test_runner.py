#!/usr/bin/env python3
"""Run a lightweight Forge field test against a real workspace.

The runner is read-only for the target workspace. It writes only to the
explicit output directory passed by the caller.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from scripts import workspace_inventory
    from scripts.agent_index_validator import validate_index
except ImportError:  # pragma: no cover - used when run directly from scripts/
    import workspace_inventory
    from agent_index_validator import validate_index


def _agent_index_result(agent_index_path: str | None) -> dict[str, Any]:
    if not agent_index_path:
        return {
            "status": "not_provided",
            "path": None,
            "errors": [],
            "warnings": [],
        }

    path = Path(agent_index_path).expanduser().resolve()
    if not path.exists() or not path.is_file():
        return {
            "status": "agent_index_invalid",
            "path": str(path),
            "errors": [f"Invalid AGENT_INDEX path: {path}"],
            "warnings": [],
        }

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "status": "agent_index_invalid",
            "path": str(path),
            "errors": [f"Invalid JSON: {exc}"],
            "warnings": [],
        }

    result = validate_index(payload)
    return {
        "status": "agent_index_valid" if result.ok else "agent_index_invalid",
        "path": str(path),
        "errors": result.errors,
        "warnings": result.warnings,
    }


def _project_lines(project: dict[str, Any]) -> list[str]:
    return [
        f"- Path: `{project['path']}`",
        f"  - Type: {project['project_type']}",
        f"  - Manifests: {', '.join(project['manifests']) or 'none'}",
        f"  - Languages: {', '.join(project['languages']) or 'unknown'}",
        f"  - Docs: {', '.join(project['docs']) or 'none'}",
        f"  - Skill signals: {', '.join(project.get('skill_signals', [])) or 'none'}",
        f"  - Run commands: {', '.join(project['run_commands']) or 'none inferred'}",
        f"  - Test commands: {', '.join(project['test_commands']) or 'none inferred'}",
        f"  - Validation commands: {', '.join(project.get('validation_commands', [])) or 'none inferred'}",
        f"  - Risks: {', '.join(project['risk_flags']) or 'none obvious'}",
    ]


def _friction_points(inventory: dict[str, Any], agent_index: dict[str, Any]) -> list[str]:
    points: list[str] = []
    status = inventory["status"]
    if status == "no_project":
        points.append("No clear project signal was detected in the target workspace.")
    if status == "multiple_projects":
        points.append("Multiple project candidates were detected; confirm the target before write-heavy work.")

    for project in inventory["projects"]:
        if not project["run_commands"] and not project.get("validation_commands"):
            points.append(f"{project['path']}: no run command was inferred.")
        if not project["test_commands"]:
            points.append(f"{project['path']}: no test command was inferred.")
        for risk in project["risk_flags"]:
            points.append(f"{project['path']}: {risk}.")

    if agent_index["status"] == "agent_index_invalid":
        points.extend(agent_index["errors"])
    return points or ["No major field-test friction detected from static evidence."]


def _suggested_improvements(inventory: dict[str, Any], agent_index: dict[str, Any]) -> list[str]:
    status = inventory["status"]
    if status == "no_project":
        return [
            "Ask the user to choose a project directory, create a scaffold, or paste project materials.",
            "Do not enter multi-agent planning until there is a concrete project or artifact set.",
        ]
    if status == "multiple_projects":
        return [
            "Ask the user to confirm the target project before editing files.",
            "Use Multi-Agent Collaboration only after ownership and write scopes are clear.",
        ]
    suggestions = [
        "Route the next step through Engineering Delivery or Review/Submit based on the detected risks.",
        "Record verification evidence before claiming the project is ready.",
    ]
    if agent_index["status"] == "agent_index_invalid":
        suggestions.insert(0, "Fix AGENT_INDEX.json before assigning work to multiple agents.")
    return suggestions


def _next_options(inventory: dict[str, Any]) -> list[dict[str, str]]:
    return inventory.get("next_options", [])


def build_result(workspace: str, max_files: int = 2000, agent_index_path: str | None = None) -> dict[str, Any]:
    inventory = workspace_inventory.scan_workspace(workspace, max_files=max_files)
    agent_index = _agent_index_result(agent_index_path)
    statuses = [inventory["status"]]
    if agent_index["status"] != "not_provided":
        statuses.append(agent_index["status"])

    routes = ["Existing Project Audit"]
    if agent_index_path or inventory["status"] == "multiple_projects":
        routes.append("Multi-Agent Collaboration")

    return {
        "schema_version": "1.0",
        "status": inventory["status"],
        "statuses": statuses,
        "workspace": inventory["workspace"],
        "triggered_routes": routes,
        "workspace_inventory": inventory,
        "agent_index": agent_index,
        "friction_points": _friction_points(inventory, agent_index),
        "suggested_improvements": _suggested_improvements(inventory, agent_index),
        "next_options": _next_options(inventory),
        "artifacts": ["FIELD_TEST_REPORT.md", "field_test.json"],
        "limits": {
            "read_only_target_workspace": True,
            "max_files": max_files,
            "model_calls": "none",
        },
    }


def build_input_error(workspace: str, exc: Exception) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "status": "input_error",
        "statuses": ["input_error"],
        "workspace": str(Path(workspace).expanduser()),
        "triggered_routes": ["Field Test Loop"],
        "workspace_inventory": None,
        "agent_index": {"status": "not_provided", "path": None, "errors": [], "warnings": []},
        "friction_points": [str(exc)],
        "suggested_improvements": [
            "Pass an existing workspace directory.",
            "If project materials are not local, paste or attach the relevant files first.",
        ],
        "next_options": [
            {"option": "选择项目目录", "why": "当前输入路径不可用。"},
            {"option": "创建新项目骨架", "why": "如果这里本来就是起点，可以先建立最小结构。"},
        ],
        "artifacts": ["FIELD_TEST_REPORT.md", "field_test.json"],
        "limits": {
            "read_only_target_workspace": True,
            "model_calls": "none",
        },
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Field Test Report",
        "",
        "功能目标：用真实工作区试跑 Forge 的自查和协作规划能力，并沉淀证据、摩擦点和下一步。",
        f"输入：{result['workspace']}",
        "输出：`FIELD_TEST_REPORT.md` 和 `field_test.json`。",
        f"状态：{', '.join(result['statuses'])}",
        "异常情况：不读取 secret 原文；不调用模型；不修改目标工程。",
        "限制：这是静态实战闭环，不代表项目已经运行、测试或交付通过。",
        "",
        "## Triggered Routes",
    ]
    lines.extend(f"- {route}" for route in result["triggered_routes"])

    lines.extend(["", "## Workspace Evidence"])
    inventory = result.get("workspace_inventory")
    if inventory:
        lines.append(f"- Workspace status: `{inventory['status']}`")
        if inventory.get("scan_notes"):
            lines.append(f"- Scan notes: {', '.join(inventory['scan_notes'])}")
        if not inventory["projects"]:
            lines.append("- 未检测到明显项目。")
        for project in inventory["projects"]:
            lines.extend(_project_lines(project))
    else:
        lines.append("- Workspace inventory was not available because input validation failed.")

    agent_index = result["agent_index"]
    lines.extend(["", "## Agent Index"])
    lines.append(f"- Status: `{agent_index['status']}`")
    if agent_index.get("path"):
        lines.append(f"- Path: `{agent_index['path']}`")
    for error in agent_index.get("errors", []):
        lines.append(f"- Error: {error}")
    for warning in agent_index.get("warnings", []):
        lines.append(f"- Warning: {warning}")

    lines.extend(["", "## Friction Points"])
    lines.extend(f"- {point}" for point in result["friction_points"])

    lines.extend(["", "## Suggested Improvements"])
    lines.extend(f"- {item}" for item in result["suggested_improvements"])

    lines.extend(["", "## 下一步选项"])
    for index, item in enumerate(result["next_options"], start=1):
        lines.append(f"{index}. {item['option']}：{item['why']}")
    lines.append("")
    return "\n".join(lines)


def _write_outputs(out_dir: Path, result: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "FIELD_TEST_REPORT.md").write_text(render_markdown(result), encoding="utf-8")
    (out_dir / "field_test.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(
    workspace: str,
    out_dir: str,
    max_files: int = 2000,
    agent_index_path: str | None = None,
) -> int:
    try:
        result = build_result(workspace, max_files=max_files, agent_index_path=agent_index_path)
        code = 1 if "agent_index_invalid" in result["statuses"] else 0
    except ValueError as exc:
        result = build_input_error(workspace, exc)
        code = 2

    try:
        _write_outputs(Path(out_dir).expanduser(), result)
    except OSError as exc:
        print(f"Failed to write field-test outputs: {exc}", file=sys.stderr)
        return 2

    print(f"Wrote {Path(out_dir).expanduser() / 'FIELD_TEST_REPORT.md'}")
    print(f"Wrote {Path(out_dir).expanduser() / 'field_test.json'}")
    if code:
        print("; ".join(result["friction_points"]), file=sys.stderr)
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a Forge field test against a real workspace.")
    parser.add_argument("workspace", help="Workspace directory to inspect")
    parser.add_argument("--out-dir", required=True, help="Directory for FIELD_TEST_REPORT.md and field_test.json")
    parser.add_argument("--max-files", type=int, default=2000, help="Max files sampled per detected project")
    parser.add_argument("--agent-index", dest="agent_index_path", help="Optional AGENT_INDEX.json to validate")
    args = parser.parse_args()
    return run(args.workspace, args.out_dir, args.max_files, args.agent_index_path)


if __name__ == "__main__":
    raise SystemExit(main())
