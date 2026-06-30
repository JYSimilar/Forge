#!/usr/bin/env python3
"""Run Forge Stable Core checks and write a doctor report."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from scripts import dual_index_builder
    from scripts import field_test_runner
except ImportError:  # pragma: no cover - used when run directly from scripts/
    import dual_index_builder
    import field_test_runner


def _release_gate(projects: list[dict[str, Any]], workspace_status: str, release: bool) -> dict[str, Any]:
    if not release:
        return {
            "enabled": False,
            "status": "not_requested",
            "evidence": [],
            "risks": [],
            "next_options": [],
        }

    evidence: list[str] = ["Release readiness requested."]
    risks: list[str] = []
    if workspace_status == "no_project":
        risks.append("release_mode: no project was detected.")
    if workspace_status == "multiple_projects":
        risks.append("release_mode: multiple projects require target confirmation before release.")

    for project in projects:
        path = project.get("path", ".")
        test_commands = project.get("test_commands", [])
        validation_commands = project.get("validation_commands", [])
        docs = project.get("docs", [])
        if test_commands:
            for command in test_commands:
                evidence.append(f"{path}: test command available: {command}")
        else:
            risks.append(f"{path}: release_mode missing test command.")
        if validation_commands:
            for command in validation_commands:
                evidence.append(f"{path}: validation command available: {command}")
        if "SKILL.md" in project.get("skill_signals", []) and not validation_commands:
            risks.append(f"{path}: skill validation command not inferred.")
        if "README.md" in docs:
            evidence.append(f"{path}: README.md present.")
        else:
            risks.append(f"{path}: release_mode missing README.md.")

    return {
        "enabled": True,
        "status": "release_mode",
        "evidence": evidence,
        "risks": risks,
        "next_options": [
            {"option": "补齐 release 风险", "why": "先处理缺失的测试、README、目标确认或校验命令。"},
            {"option": "运行完整验证", "why": "发布前需要用实际命令确认报告中的验证线索。"},
            {"option": "准备 tag 和发布说明", "why": "验证通过后再进入 Review/Submit 与 Release Readiness。"},
        ],
    }


def build_input_error(workspace: str, exc: Exception) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "status": "input_error",
        "statuses": ["input_error"],
        "workspace": str(Path(workspace).expanduser()),
        "source_routes": ["Stability Gate"],
        "artifacts": {
            "doctor_report": "FORGE_DOCTOR_REPORT.md",
            "doctor_json": "forge_doctor.json",
        },
        "projects": [],
        "field_test": None,
        "release_readiness": {"enabled": False, "status": "not_available", "evidence": [], "risks": []},
        "evidence": [],
        "risks": [str(exc)],
        "next_options": [
            {"option": "选择项目目录", "why": "当前输入路径不可用。"},
            {"option": "粘贴资料", "why": "如果项目不在本机，可以先用资料建立稳定性检查。"},
        ],
        "limits": {
            "read_only_target_workspace": True,
            "model_calls": "none",
            "writes_only_out_dir": True,
        },
    }


def build_result(
    workspace: str,
    max_files: int = 2000,
    agent_index_path: str | None = None,
    router_contract_path: str | None = None,
    field_test_json_path: str | None = None,
    release: bool = False,
) -> tuple[dict[str, Any], int]:
    dual_payload, dual_code = dual_index_builder.build_payload(
        workspace,
        max_files=max_files,
        agent_index_path=agent_index_path,
        router_contract_path=router_contract_path,
        field_test_json_path=field_test_json_path,
    )
    try:
        field_test = field_test_runner.build_result(workspace, max_files=max_files, agent_index_path=agent_index_path)
    except ValueError:
        field_test = None

    release_gate = _release_gate(dual_payload["projects"], dual_payload["status"], release)
    statuses = ["forge_doctor", *dual_payload["statuses"]]
    if release_gate["enabled"]:
        statuses.append("release_mode")
    if field_test and "field_test_loop" not in statuses:
        statuses.append("field_test_loop")

    evidence = [
        "workspace inventory collected",
        "dual index payload built from one fact source",
    ]
    evidence.extend(dual_payload["evidence"])
    if field_test:
        evidence.append(f"field_test_status={field_test['status']}")
    evidence.extend(release_gate["evidence"])

    risks = list(dual_payload["risks"])
    if field_test:
        for point in field_test.get("friction_points", []):
            if point != "No major field-test friction detected from static evidence.":
                risks.append(str(point))
    risks.extend(release_gate["risks"])

    artifacts = {
        "doctor_report": "FORGE_DOCTOR_REPORT.md",
        "doctor_json": "forge_doctor.json",
        "human_index": "FORGE_INDEX.md",
        "machine_index": "forge_index.json",
        "field_test_report": "FIELD_TEST_REPORT.md",
        "router_test_report": "ROUTER_TEST_REPORT.md",
    }
    payload = {
        "schema_version": "1.0",
        "status": dual_payload["status"],
        "statuses": statuses,
        "workspace": dual_payload["workspace"],
        "source_routes": ["Stability Gate", *dual_payload["source_routes"]],
        "artifacts": artifacts,
        "projects": dual_payload["projects"],
        "field_test": field_test,
        "release_readiness": release_gate,
        "evidence": evidence,
        "risks": risks,
        "next_options": release_gate["next_options"] or dual_payload["next_options"],
        "limits": {
            "read_only_target_workspace": True,
            "max_files": max_files,
            "model_calls": "none",
            "writes_only_out_dir": True,
            "optional_invalid_indexes_return_code": 1,
        },
    }
    code = 1 if dual_code == 1 else 0
    return payload, code


def render_markdown(payload: dict[str, Any]) -> str:
    status_line = ", ".join(payload["statuses"])
    lines = [
        "# Forge Doctor Report",
        "",
        "功能目标：运行 Forge 2.0 Stable Core 自检，汇总工作区、路由、双索引、协作索引、field test 和发布门禁证据。",
        f"输入：{payload['workspace']}",
        "输出：`FORGE_DOCTOR_REPORT.md` 和 `forge_doctor.json`。",
        f"状态：{status_line}",
        "异常情况：无效的可选索引会标记为风险并返回非零码；不会误报成功。",
        "限制：目标 workspace 只读；不读取 secret 原文；不调用模型；只写指定输出目录。",
        "",
        "## Route Evidence",
    ]
    for route in payload["source_routes"]:
        lines.append(f"- {route}")

    lines.extend(["", "## Workspace"])
    if not payload["projects"]:
        lines.append("- 未检测到明显项目。")
    for project in payload["projects"]:
        lines.extend(
            [
                f"- Path: `{project['path']}`",
                f"  - Type: {project['project_type']}",
                f"  - Manifests: {', '.join(project['manifests']) or 'none'}",
                f"  - Test commands: {', '.join(project['test_commands']) or 'none inferred'}",
                f"  - Validation commands: {', '.join(project.get('validation_commands', [])) or 'none inferred'}",
                f"  - Risks: {', '.join(project['risk_flags']) or 'none obvious'}",
            ]
        )

    release_gate = payload["release_readiness"]
    lines.extend(["", "## Release readiness"])
    lines.append(f"- Enabled: {release_gate['enabled']}")
    lines.append(f"- Status: `{release_gate['status']}`")
    for item in release_gate.get("evidence", []):
        lines.append(f"- Evidence: {item}")
    for item in release_gate.get("risks", []):
        lines.append(f"- Risk: {item}")

    lines.extend(["", "## 验证证据"])
    if payload["evidence"]:
        lines.extend(f"- {item}" for item in payload["evidence"])
    else:
        lines.append("- No evidence collected.")

    lines.extend(["", "## 风险"])
    if payload["risks"]:
        lines.extend(f"- {item}" for item in payload["risks"])
    else:
        lines.append("- none obvious")

    lines.extend(["", "## 产物索引"])
    for key, value in sorted(payload["artifacts"].items()):
        lines.append(f"- {key}: `{value}`")

    lines.extend(["", "## 下一步选项"])
    for index, item in enumerate(payload["next_options"], start=1):
        lines.append(f"{index}. {item['option']}：{item['why']}")
    lines.append("")
    return "\n".join(lines)


def _write_outputs(out_dir: Path, payload: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "FORGE_DOCTOR_REPORT.md").write_text(render_markdown(payload), encoding="utf-8")
    (out_dir / "forge_doctor.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(
    workspace: str,
    out_dir: str,
    max_files: int = 2000,
    agent_index_path: str | None = None,
    router_contract_path: str | None = None,
    field_test_json_path: str | None = None,
    release: bool = False,
) -> int:
    try:
        payload, code = build_result(
            workspace,
            max_files=max_files,
            agent_index_path=agent_index_path,
            router_contract_path=router_contract_path,
            field_test_json_path=field_test_json_path,
            release=release,
        )
    except ValueError as exc:
        payload = build_input_error(workspace, exc)
        code = 2

    try:
        _write_outputs(Path(out_dir).expanduser(), payload)
    except OSError as exc:
        print(f"Failed to write Forge Doctor outputs: {exc}", file=sys.stderr)
        return 2

    print(f"Wrote {Path(out_dir).expanduser() / 'FORGE_DOCTOR_REPORT.md'}")
    print(f"Wrote {Path(out_dir).expanduser() / 'forge_doctor.json'}")
    if code:
        print("; ".join(payload["risks"]), file=sys.stderr)
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Forge 2.0 Stable Core checks and write a doctor report.")
    parser.add_argument("workspace", help="Workspace directory to inspect")
    parser.add_argument("--out-dir", required=True, help="Directory for FORGE_DOCTOR_REPORT.md and forge_doctor.json")
    parser.add_argument("--max-files", type=int, default=2000, help="Max files sampled per detected project")
    parser.add_argument("--agent-index", dest="agent_index_path", help="Optional AGENT_INDEX.json to validate")
    parser.add_argument("--router-contract", dest="router_contract_path", help="Optional ROUTER_CONTRACT.json to validate")
    parser.add_argument("--field-test-json", dest="field_test_json_path", help="Optional field_test.json to include")
    parser.add_argument("--release", action="store_true", help="Enable release-readiness checks")
    args = parser.parse_args()
    return run(
        args.workspace,
        args.out_dir,
        args.max_files,
        args.agent_index_path,
        args.router_contract_path,
        args.field_test_json_path,
        args.release,
    )


if __name__ == "__main__":
    raise SystemExit(main())
