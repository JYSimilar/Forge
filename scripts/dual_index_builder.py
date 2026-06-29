#!/usr/bin/env python3
"""Build Forge human and machine indexes from one shared fact payload."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from scripts import workspace_inventory
    from scripts.agent_index_validator import validate_index
    from scripts import router_contract_validator
except ImportError:  # pragma: no cover - used when run directly from scripts/
    import workspace_inventory
    from agent_index_validator import validate_index
    import router_contract_validator


def _load_json(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"Invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return None, ["top-level JSON must be an object"]
    return payload, []


def _agent_index_payload(agent_index_path: str | None) -> dict[str, Any]:
    if not agent_index_path:
        return {"status": "not_provided", "path": None, "errors": [], "warnings": [], "payload": None}

    path = Path(agent_index_path).expanduser().resolve()
    if not path.exists() or not path.is_file():
        return {
            "status": "agent_index_invalid",
            "path": str(path),
            "errors": [f"Invalid AGENT_INDEX path: {path}"],
            "warnings": [],
            "payload": None,
        }
    payload, errors = _load_json(path)
    if errors:
        return {"status": "agent_index_invalid", "path": str(path), "errors": errors, "warnings": [], "payload": None}

    result = validate_index(payload)
    return {
        "status": "agent_index_valid" if result.ok else "agent_index_invalid",
        "path": str(path),
        "errors": result.errors,
        "warnings": result.warnings,
        "payload": payload if result.ok else None,
    }


def _router_contract_payload(router_contract_path: str | None) -> dict[str, Any]:
    if not router_contract_path:
        return {"status": "not_provided", "path": None, "errors": [], "warnings": [], "payload": None}

    path = Path(router_contract_path).expanduser().resolve()
    if not path.exists() or not path.is_file():
        return {
            "status": "router_contract_invalid",
            "path": str(path),
            "errors": [f"Invalid ROUTER_CONTRACT path: {path}"],
            "warnings": [],
            "payload": None,
        }
    payload, errors = _load_json(path)
    if errors:
        return {
            "status": "router_contract_invalid",
            "path": str(path),
            "errors": errors,
            "warnings": [],
            "payload": None,
        }

    result = router_contract_validator.validate_contract(
        payload,
        base_dir=router_contract_validator._find_repo_root(path),  # noqa: SLF001 - reuse script-local repo detection.
    )
    return {
        "status": "router_contract_valid" if result.ok else "router_contract_invalid",
        "path": str(path),
        "errors": result.errors,
        "warnings": result.warnings,
        "payload": payload if result.ok else None,
    }


def _field_test_payload(field_test_json_path: str | None) -> dict[str, Any]:
    if not field_test_json_path:
        return {"status": "not_provided", "path": None, "errors": [], "payload": None}

    path = Path(field_test_json_path).expanduser().resolve()
    if not path.exists() or not path.is_file():
        return {
            "status": "field_test_json_invalid",
            "path": str(path),
            "errors": [f"Invalid field_test.json path: {path}"],
            "payload": None,
        }
    payload, errors = _load_json(path)
    if errors:
        return {"status": "field_test_json_invalid", "path": str(path), "errors": errors, "payload": None}
    return {"status": "field_test_json_loaded", "path": str(path), "errors": [], "payload": payload}


def _project_risks(projects: list[dict[str, Any]]) -> list[str]:
    risks: list[str] = []
    for project in projects:
        for risk in project.get("risk_flags", []):
            risks.append(f"{project['path']}: {risk}")
    return risks


def _evidence_from_projects(projects: list[dict[str, Any]]) -> list[str]:
    evidence: list[str] = []
    for project in projects:
        for command in project.get("run_commands", []):
            evidence.append(f"{project['path']}: run={command}")
        for command in project.get("test_commands", []):
            evidence.append(f"{project['path']}: test={command}")
        for command in project.get("validation_commands", []):
            evidence.append(f"{project['path']}: validation={command}")
    return evidence


def _summarize_routes(router_payload: dict[str, Any] | None) -> list[dict[str, str]]:
    if not router_payload:
        return []
    routes = router_payload.get("routes", [])
    if not isinstance(routes, list):
        return []
    summary: list[dict[str, str]] = []
    for route in routes:
        if not isinstance(route, dict):
            continue
        summary.append(
            {
                "id": str(route.get("id", "")),
                "name": str(route.get("name", "")),
                "minimum_reference": str(route.get("minimum_reference", "")),
                "token_mode_default": str(route.get("token_mode_default", "")),
            }
        )
    return summary


def build_payload(
    workspace: str,
    max_files: int = 2000,
    agent_index_path: str | None = None,
    router_contract_path: str | None = None,
    field_test_json_path: str | None = None,
) -> tuple[dict[str, Any], int]:
    inventory = workspace_inventory.scan_workspace(workspace, max_files=max_files)
    agent_index = _agent_index_payload(agent_index_path)
    router_contract = _router_contract_payload(router_contract_path)
    field_test = _field_test_payload(field_test_json_path)

    statuses = [inventory["status"]]
    for item in (agent_index, router_contract, field_test):
        if item["status"] != "not_provided":
            statuses.append(item["status"])

    source_routes = ["Dual Index", "Existing Project Audit"]
    field_payload = field_test.get("payload")
    if isinstance(field_payload, dict):
        for route in field_payload.get("triggered_routes", []):
            if isinstance(route, str) and route not in source_routes:
                source_routes.append(route)
    if agent_index_path and "Multi-Agent Collaboration" not in source_routes:
        source_routes.append("Multi-Agent Collaboration")
    if router_contract_path and "Router Contract" not in source_routes:
        source_routes.append("Router Contract")

    risks = _project_risks(inventory["projects"])
    for item in (agent_index, router_contract, field_test):
        risks.extend(item.get("errors", []))
    if isinstance(field_payload, dict):
        risks.extend(str(item) for item in field_payload.get("friction_points", []) if isinstance(item, str))

    evidence = _evidence_from_projects(inventory["projects"])
    if agent_index["status"] != "not_provided":
        evidence.append(f"agent_index={agent_index['status']}")
    if router_contract["status"] != "not_provided":
        evidence.append(f"router_contract={router_contract['status']}")
    if field_test["status"] != "not_provided":
        evidence.append(f"field_test_json={field_test['status']}")

    agent_payload = agent_index.get("payload") or {}
    agents = agent_payload.get("agents", []) if isinstance(agent_payload, dict) else []
    tasks = agent_payload.get("tasks", []) if isinstance(agent_payload, dict) else []

    payload = {
        "schema_version": "1.0",
        "status": inventory["status"],
        "statuses": statuses,
        "workspace": inventory["workspace"],
        "source_routes": source_routes,
        "artifacts": {
            "human_index": "FORGE_INDEX.md",
            "machine_index": "forge_index.json",
            "workspace_summary": "WORKSPACE_SUMMARY.md",
            "multi_agent_plan": "MULTI_AGENT_PLAN.md",
            "agent_index": "AGENT_INDEX.json",
            "field_test_report": "FIELD_TEST_REPORT.md",
        },
        "projects": inventory["projects"],
        "agents": agents if isinstance(agents, list) else [],
        "tasks": tasks if isinstance(tasks, list) else [],
        "routes": _summarize_routes(router_contract.get("payload")),
        "evidence": evidence,
        "risks": risks,
        "next_options": inventory["next_options"],
        "limits": {
            "read_only_target_workspace": True,
            "max_files": max_files,
            "model_calls": "none",
            "single_payload_source": True,
        },
    }

    code = 1 if any(status.endswith("_invalid") for status in statuses) else 0
    return payload, code


def build_input_error(workspace: str, exc: Exception) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "status": "input_error",
        "statuses": ["input_error"],
        "workspace": str(Path(workspace).expanduser()),
        "source_routes": ["Dual Index"],
        "artifacts": {
            "human_index": "FORGE_INDEX.md",
            "machine_index": "forge_index.json",
        },
        "projects": [],
        "agents": [],
        "tasks": [],
        "routes": [],
        "evidence": [],
        "risks": [str(exc)],
        "next_options": [
            {"option": "选择项目目录", "why": "当前输入路径不可用。"},
            {"option": "粘贴已有资料", "why": "如果项目不在本机，可以先用资料生成索引。"},
        ],
        "limits": {
            "read_only_target_workspace": True,
            "model_calls": "none",
            "single_payload_source": True,
        },
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Forge Index",
        "",
        "功能目标：同时生成给人看的 Markdown 索引和给 AI/脚本看的 JSON 索引，并保证二者来自同一份事实 payload。",
        f"输入：{payload['workspace']}",
        "输出：`FORGE_INDEX.md` 和 `forge_index.json`。",
        f"状态：{payload['status']}",
        "异常情况：无效的可选索引会被标记为风险，不会误报成功。",
        "限制：目标 workspace 只读；不读取 secret 原文；不调用模型。",
        "",
        "## 路线摘要",
    ]
    lines.extend(f"- {route}" for route in payload["source_routes"])

    lines.extend(["", "## 项目摘要"])
    if not payload["projects"]:
        lines.append("- 未检测到明显项目。")
    for project in payload["projects"]:
        lines.extend(
            [
                f"- Path: `{project['path']}`",
                f"  - Type: {project['project_type']}",
                f"  - Manifests: {', '.join(project['manifests']) or 'none'}",
                f"  - Languages: {', '.join(project['languages']) or 'unknown'}",
                f"  - Test commands: {', '.join(project['test_commands']) or 'none inferred'}",
                f"  - Validation commands: {', '.join(project.get('validation_commands', [])) or 'none inferred'}",
                f"  - Risks: {', '.join(project['risk_flags']) or 'none obvious'}",
            ]
        )

    lines.extend(["", "## 产物索引"])
    artifacts = payload["artifacts"]
    for key in sorted(artifacts):
        lines.append(f"- {key}: `{artifacts[key]}`")

    lines.extend(["", "## Agent / Task 摘要"])
    if not payload["agents"] and not payload["tasks"]:
        lines.append("- No agent index loaded.")
    for agent in payload["agents"]:
        lines.append(f"- Agent `{agent.get('id')}`: {agent.get('role')} / {agent.get('status')}")
    for task in payload["tasks"]:
        lines.append(f"- Task `{task.get('id')}`: {task.get('title')} / {task.get('status')}")

    lines.extend(["", "## Router 摘要"])
    if not payload["routes"]:
        lines.append("- No router contract loaded.")
    else:
        lines.append(f"- Status: `{next((status for status in payload['statuses'] if status.startswith('router_contract_')), 'not_provided')}`")
        for route in payload["routes"]:
            lines.append(f"- `{route['id']}` -> {route['minimum_reference']}")

    lines.extend(["", "## 验证证据"])
    if payload["evidence"]:
        lines.extend(f"- {item}" for item in payload["evidence"])
    else:
        lines.append("- No run/test/validation evidence inferred.")

    lines.extend(["", "## 风险"])
    if payload["risks"]:
        lines.extend(f"- {item}" for item in payload["risks"])
    else:
        lines.append("- none obvious")

    lines.extend(["", "## 下一步选项"])
    for index, item in enumerate(payload["next_options"], start=1):
        lines.append(f"{index}. {item['option']}：{item['why']}")
    lines.append("")
    return "\n".join(lines)


def _write_outputs(out_dir: Path, payload: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "FORGE_INDEX.md").write_text(render_markdown(payload), encoding="utf-8")
    (out_dir / "forge_index.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(
    workspace: str,
    out_dir: str,
    max_files: int = 2000,
    agent_index_path: str | None = None,
    router_contract_path: str | None = None,
    field_test_json_path: str | None = None,
) -> int:
    try:
        payload, code = build_payload(
            workspace,
            max_files=max_files,
            agent_index_path=agent_index_path,
            router_contract_path=router_contract_path,
            field_test_json_path=field_test_json_path,
        )
    except ValueError as exc:
        payload = build_input_error(workspace, exc)
        code = 2

    try:
        _write_outputs(Path(out_dir).expanduser(), payload)
    except OSError as exc:
        print(f"Failed to write dual-index outputs: {exc}", file=sys.stderr)
        return 2

    print(f"Wrote {Path(out_dir).expanduser() / 'FORGE_INDEX.md'}")
    print(f"Wrote {Path(out_dir).expanduser() / 'forge_index.json'}")
    if code:
        print("; ".join(payload["risks"]), file=sys.stderr)
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Forge human and machine indexes from one fact payload.")
    parser.add_argument("workspace", help="Workspace directory to inspect")
    parser.add_argument("--out-dir", required=True, help="Directory for FORGE_INDEX.md and forge_index.json")
    parser.add_argument("--max-files", type=int, default=2000, help="Max files sampled per detected project")
    parser.add_argument("--agent-index", dest="agent_index_path", help="Optional AGENT_INDEX.json to validate and include")
    parser.add_argument(
        "--router-contract",
        dest="router_contract_path",
        help="Optional ROUTER_CONTRACT.json to validate and include",
    )
    parser.add_argument("--field-test-json", dest="field_test_json_path", help="Optional field_test.json to include")
    args = parser.parse_args()
    return run(
        args.workspace,
        args.out_dir,
        args.max_files,
        args.agent_index_path,
        args.router_contract_path,
        args.field_test_json_path,
    )


if __name__ == "__main__":
    raise SystemExit(main())
