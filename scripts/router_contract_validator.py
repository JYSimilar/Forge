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


@dataclass
class CorpusResult:
    cases: list[dict[str, Any]]
    errors: list[str]
    warnings: list[str]
    summary: dict[str, Any]

    @property
    def ok(self) -> bool:
        return not self.errors


DUAL_INDEX_ROUTE_IDS = {
    "existing_project_audit",
    "field_test_loop",
    "multi_agent_collaboration",
    "router_contract",
    "pluginization_roadmap",
    "release_readiness",
    "dual_index",
    "stability_gate",
}
BURN_TRIGGERS = ("燃烧模式", "burn mode", "燃烧 token")
STANDARD_DEEP_TRIGGERS = ("详细一点", "展开说说")


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


def load_corpus(corpus_path: str | Path) -> dict[str, Any]:
    path = Path(corpus_path).expanduser()
    with path.open("r", encoding="utf-8") as handle:
        return _expand_corpus(json.load(handle))


def _expand_corpus(corpus: Any) -> dict[str, Any]:
    """Expand compact scenario sets into ordinary deterministic corpus cases."""
    if not isinstance(corpus, dict):
        return corpus
    expanded = dict(corpus)
    scenarios = list(corpus.get("scenarios", []))
    scenario_sets = corpus.get("scenario_sets", [])
    if not isinstance(scenario_sets, list):
        return expanded
    for set_index, scenario_set in enumerate(scenario_sets):
        if not isinstance(scenario_set, dict):
            scenarios.append({"id": f"invalid_set_{set_index}"})
            continue
        prefix = scenario_set.get("id_prefix", f"set_{set_index}")
        prompts = scenario_set.get("prompts", [])
        if not isinstance(prefix, str) or not isinstance(prompts, list):
            scenarios.append({"id": f"invalid_set_{set_index}"})
            continue
        for prompt_index, prompt in enumerate(prompts, start=1):
            scenario = {
                key: value
                for key, value in scenario_set.items()
                if key not in {"id_prefix", "prompts"}
            }
            scenario["id"] = f"{prefix}_{prompt_index:02d}"
            scenario["prompt"] = prompt
            scenarios.append(scenario)
    expanded["scenarios"] = scenarios
    return expanded


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

    token_mode = str(best_route.get("token_mode_default", ""))
    if any(trigger in prompt_norm for trigger in BURN_TRIGGERS):
        token_mode = "Burn Mode"
    elif any(trigger in prompt_norm for trigger in STANDARD_DEEP_TRIGGERS):
        token_mode = "Standard Deep"

    return RouteDecision(
        route_id=str(best_route.get("id", "unknown")),
        score=max(best_score, 0),
        matched_triggers=best_matches,
        token_mode=token_mode,
        minimum_reference=str(best_route.get("minimum_reference", "")),
    )


def _should_generate_dual_index(decision: RouteDecision, prompt: str) -> bool:
    prompt_norm = _normalize(prompt)
    if "不要生成索引" in prompt_norm or "不要索引" in prompt_norm or "skip index" in prompt_norm:
        return False
    return decision.route_id in DUAL_INDEX_ROUTE_IDS


def _validate_corpus(corpus: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(corpus, dict):
        return ["corpus top-level JSON must be an object"]
    _expect_text(corpus, "schema_version", "corpus", errors)
    scenarios = corpus.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        errors.append("corpus.scenarios must be a non-empty list")
        return errors
    seen_ids: set[str] = set()
    for index, scenario in enumerate(scenarios):
        label = f"scenarios[{index}]"
        if not isinstance(scenario, dict):
            errors.append(f"{label} must be an object")
            continue
        for key in ("id", "prompt", "expected_route_id", "expected_token_mode"):
            _expect_text(scenario, key, label, errors)
        if not isinstance(scenario.get("expected_dual_index"), bool):
            errors.append(f"{label}.expected_dual_index must be a boolean")
        scenario_id = scenario.get("id")
        if _is_text(scenario_id):
            if scenario_id in seen_ids:
                errors.append(f"{label}.id duplicates scenario id {scenario_id!r}")
            seen_ids.add(scenario_id)
    return errors


def _corpus_summary(cases: list[dict[str, Any]]) -> dict[str, Any]:
    routes: dict[str, dict[str, Any]] = {}
    confusion_counts: dict[str, int] = {}
    passed = 0
    for case in cases:
        expected = str(case["expected_route_id"])
        route = routes.setdefault(expected, {"total": 0, "passed": 0, "failed": 0, "accuracy": 0.0})
        route["total"] += 1
        if case["passed"]:
            passed += 1
            route["passed"] += 1
        else:
            route["failed"] += 1
            pair = f"{expected} -> {case['actual_route_id']}"
            confusion_counts[pair] = confusion_counts.get(pair, 0) + 1
    for route in routes.values():
        route["accuracy"] = round(route["passed"] / route["total"], 4) if route["total"] else 0.0
    return {
        "total": len(cases),
        "passed": passed,
        "failed": len(cases) - passed,
        "accuracy": round(passed / len(cases), 4) if cases else 0.0,
        "routes": dict(sorted(routes.items())),
        "confusion_pairs": [
            {"pair": pair, "count": count}
            for pair, count in sorted(confusion_counts.items(), key=lambda item: (-item[1], item[0]))
        ],
    }


def run_corpus(payload: dict[str, Any], corpus: Any) -> CorpusResult:
    errors = _validate_corpus(corpus)
    if errors:
        return CorpusResult([], errors, [], _corpus_summary([]))

    route_ids = {route.get("id") for route in payload.get("routes", []) if isinstance(route, dict)}
    cases: list[dict[str, Any]] = []
    for scenario in corpus["scenarios"]:
        expected_route = str(scenario["expected_route_id"])
        if expected_route not in route_ids:
            errors.append(f"{scenario['id']}: expected_route_id {expected_route!r} is not in router contract")
            continue
        decision = simulate_route(payload, str(scenario["prompt"]))
        actual_dual_index = _should_generate_dual_index(decision, str(scenario["prompt"]))
        case = {
            "id": str(scenario["id"]),
            "prompt": str(scenario["prompt"]),
            "expected_route_id": expected_route,
            "actual_route_id": decision.route_id,
            "expected_token_mode": str(scenario["expected_token_mode"]),
            "actual_token_mode": decision.token_mode,
            "expected_dual_index": bool(scenario["expected_dual_index"]),
            "actual_dual_index": actual_dual_index,
            "matched_triggers": decision.matched_triggers,
            "language": str(scenario.get("language", "unspecified")),
            "intent": str(scenario.get("intent", "unspecified")),
            "ambiguity": str(scenario.get("ambiguity", "none")),
            "passed": True,
        }
        failures: list[str] = []
        if decision.route_id != expected_route:
            failures.append(f"route expected {expected_route}, got {decision.route_id}")
        if decision.token_mode != case["expected_token_mode"]:
            failures.append(f"token mode expected {case['expected_token_mode']}, got {decision.token_mode}")
        if actual_dual_index != case["expected_dual_index"]:
            failures.append(
                f"dual index expected {case['expected_dual_index']}, got {actual_dual_index}"
            )
        if failures:
            case["passed"] = False
            case["failures"] = failures
            errors.extend(f"{case['id']}: {failure}" for failure in failures)
        cases.append(case)
    return CorpusResult(cases, errors, [], _corpus_summary(cases))


def render_corpus_report(result: CorpusResult, contract_path: Path, corpus_path: Path) -> str:
    status = "passed" if result.ok else "failed"
    lines = [
        "# Router Test Report",
        "",
        "功能目标：批量验证自然调用是否仍路由到预期 Forge 能力，并检查 token 模式和双索引触发预期。",
        f"输入：`{contract_path}` + `{corpus_path}`",
        "输出：Router corpus regression report.",
        f"状态：{status}",
        "异常情况：失败样例会列出实际路线、token 模式或双索引触发差异。",
        "限制：本报告只做本地确定性模拟，不调用模型。",
        "评测说明：这是路由契约回归集，不代表模型语义理解准确率。",
        "",
        "## Summary",
        f"- Total: {result.summary['total']}",
        f"- Passed: {result.summary['passed']}",
        f"- Failed: {result.summary['failed']}",
        f"- Accuracy: {result.summary['accuracy']:.2%}",
        "",
        "## Route Metrics",
    ]
    for route_id, metrics in result.summary["routes"].items():
        lines.append(
            f"- `{route_id}`: {metrics['passed']}/{metrics['total']} passed "
            f"({metrics['accuracy']:.2%}), failed={metrics['failed']}"
        )
    lines.extend(["", "## Confusion Pairs"])
    if result.summary["confusion_pairs"]:
        for item in result.summary["confusion_pairs"]:
            lines.append(f"- {item['pair']}: {item['count']}")
    else:
        lines.append("- none")
    lines.extend(["", "## Cases"])
    for case in result.cases:
        marker = "PASS" if case["passed"] else "FAIL"
        lines.append(
            f"- {marker} `{case['id']}`: route {case['actual_route_id']} "
            f"(expected {case['expected_route_id']}), token {case['actual_token_mode']} "
            f"(expected {case['expected_token_mode']}), dual_index={case['actual_dual_index']}"
        )
        for failure in case.get("failures", []):
            lines.append(f"  - {failure}")
    if result.errors:
        lines.extend(["", "## Errors"])
        lines.extend(f"- {error}" for error in result.errors)
    lines.append("")
    return "\n".join(lines)


def run(
    contract_path: str | Path,
    simulate_prompt: str | None = None,
    corpus_path: str | Path | None = None,
    report_path: str | Path | None = None,
) -> int:
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

    if corpus_path:
        corpus_file = Path(corpus_path).expanduser()
        if not corpus_file.exists() or not corpus_file.is_file():
            print(f"Invalid router prompt corpus path: {corpus_file}", file=sys.stderr)
            return 2
        try:
            corpus = load_corpus(corpus_file)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Invalid corpus JSON: {exc}", file=sys.stderr)
            return 2
        corpus_result = run_corpus(payload, corpus)
        if report_path:
            try:
                report_file = Path(report_path).expanduser()
                report_file.parent.mkdir(parents=True, exist_ok=True)
                report_file.write_text(render_corpus_report(corpus_result, path, corpus_file), encoding="utf-8")
            except OSError as exc:
                print(f"Failed to write router test report: {exc}", file=sys.stderr)
                return 2
        if not corpus_result.ok:
            print("Router prompt corpus failed.", file=sys.stderr)
            for error in corpus_result.errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print(f"Router prompt corpus passed ({len(corpus_result.cases)} scenarios).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and simulate a Forge ROUTER_CONTRACT.json file.")
    parser.add_argument("contract", help="Path to ROUTER_CONTRACT.json")
    parser.add_argument("--simulate", help="Prompt to route through the contract")
    parser.add_argument("--corpus", dest="corpus_path", help="Optional ROUTER_PROMPT_CORPUS.json to batch validate")
    parser.add_argument("--report", dest="report_path", help="Optional Markdown report path for corpus validation")
    args = parser.parse_args()
    return run(args.contract, args.simulate, args.corpus_path, args.report_path)


if __name__ == "__main__":
    raise SystemExit(main())
