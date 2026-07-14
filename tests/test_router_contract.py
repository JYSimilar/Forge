import copy
import importlib
import io
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_router_validator():
    return importlib.import_module("scripts.router_contract_validator")


class RouterContractTests(unittest.TestCase):
    def test_router_contract_files_are_indexed(self):
        self.assertTrue((ROOT / "references" / "router-contract.md").exists())
        self.assertTrue((ROOT / "assets" / "templates" / "ROUTER_CONTRACT.json").exists())
        self.assertTrue((ROOT / "assets" / "templates" / "ROUTER_CONTRACT.md").exists())
        self.assertTrue((ROOT / "assets" / "templates" / "ROUTER_TEST_REPORT.md").exists())
        self.assertTrue((ROOT / "scripts" / "router_contract_validator.py").exists())

        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        index = (ROOT / "INDEX.md").read_text(encoding="utf-8")
        triggers = (ROOT / "references" / "trigger-examples.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "references" / "pluginization-roadmap.md").read_text(encoding="utf-8")

        for text in (skill, index, triggers, roadmap):
            self.assertIn("router-contract.md", text)
        self.assertIn("ROUTER_CONTRACT.json", index)
        self.assertIn("ROUTER_TEST_REPORT.md", index)

    def test_template_contract_validates_and_declares_core_routes(self):
        module = load_router_validator()
        payload = module.load_contract(ROOT / "assets" / "templates" / "ROUTER_CONTRACT.json")

        result = module.validate_contract(payload)

        self.assertEqual([], result.errors)
        self.assertTrue(result.ok)
        route_ids = {route["id"] for route in payload["routes"]}
        for expected in {
            "lite",
            "single_host_role_protocol",
            "manual_handoff_notes",
            "boundary_clarification",
            "context_budget_contract",
            "existing_project_audit",
            "field_test_loop",
            "multi_agent_collaboration",
            "pluginization_roadmap",
            "router_contract",
            "dual_index",
            "stability_gate",
            "release_readiness",
            "review_submit",
        }:
            self.assertIn(expected, route_ids)
        release_route = next(route for route in payload["routes"] if route["id"] == "release_readiness")
        self.assertEqual("references/release-readiness.md", release_route["minimum_reference"])

    def test_invalid_contract_reports_missing_required_route_fields(self):
        module = load_router_validator()
        payload = module.load_contract(ROOT / "assets" / "templates" / "ROUTER_CONTRACT.json")
        invalid = copy.deepcopy(payload)
        del invalid["routes"][0]["completion_evidence"]

        result = module.validate_contract(invalid)

        self.assertFalse(result.ok)
        self.assertTrue(any("completion_evidence" in error for error in result.errors))

    def test_invalid_contract_reports_missing_reference_paths(self):
        module = load_router_validator()
        payload = module.load_contract(ROOT / "assets" / "templates" / "ROUTER_CONTRACT.json")
        invalid = copy.deepcopy(payload)
        invalid["routes"][0]["minimum_reference"] = "references/missing-route.md"

        result = module.validate_contract(invalid, base_dir=ROOT)

        self.assertFalse(result.ok)
        self.assertTrue(any("missing-route.md" in error for error in result.errors))

    def test_simulates_natural_route_selection(self):
        module = load_router_validator()
        payload = module.load_contract(ROOT / "assets" / "templates" / "ROUTER_CONTRACT.json")

        scenarios = [
            ("只给我 commit message", "lite"),
            ("这个仓库有什么问题？", "existing_project_audit"),
            ("对这个 Skill 仓库跑一轮 field test", "field_test_loop"),
            ("在当前 agent 里让前端后端测试几个角色分工", "multi_agent_collaboration"),
            ("先不要拆实现，设计 router skill + 子 skill", "pluginization_roadmap"),
            ("按 RELEASE_CHECKLIST 检查这版能不能打 tag 发布", "release_readiness"),
            ("帮我看这次改动能不能提交", "review_submit"),
            ("检查这些自然调用会不会路由到正确能力", "router_contract"),
            ("这个 Skill 项目试跑一下实战闭环", "field_test_loop"),
            ("这几个角色怎么分工协作", "multi_agent_collaboration"),
            ("这个自然触发会不会走错能力", "router_contract"),
            ("修复前端页面的登录按钮", "engineering_delivery"),
            ("给我同时生成人类索引和机器索引", "dual_index"),
            ("输出给人看的 md 和 AI 看的 json", "dual_index"),
            ("在当前 agent 里生成一个角色任务单", "single_host_role_protocol"),
            ("给当前 Codex 执行的 work order", "single_host_role_protocol"),
            ("手动复制给 Claude Code 的任务单", "manual_handoff_notes"),
            ("让 Codex 调 Claude 做 review", "boundary_clarification"),
            ("自动让几个模型并行做", "boundary_clarification"),
            ("这个任务怎么控制上下文", "context_budget_contract"),
            ("不要多 agent，生成一个通用 agent 任务单", "single_host_role_protocol"),
        ]

        for prompt, expected_route in scenarios:
            with self.subTest(prompt=prompt):
                decision = module.simulate_route(payload, prompt)
                self.assertEqual(expected_route, decision.route_id)
                self.assertGreater(decision.score, 0)

    def test_prompt_corpus_validates_route_regressions(self):
        module = load_router_validator()
        payload = module.load_contract(ROOT / "assets" / "templates" / "ROUTER_CONTRACT.json")
        corpus = module.load_corpus(ROOT / "assets" / "templates" / "ROUTER_PROMPT_CORPUS.json")

        result = module.run_corpus(payload, corpus)

        self.assertTrue(result.ok, result.errors)
        self.assertGreaterEqual(len(result.cases), 100)
        self.assertTrue(any(case["expected_dual_index"] is True for case in result.cases))
        self.assertTrue(any(case["expected_token_mode"] == "Burn Mode" for case in result.cases))
        self.assertEqual(len(result.cases), result.summary["total"])
        self.assertEqual(len(result.cases), result.summary["passed"])
        self.assertEqual(0, result.summary["failed"])
        self.assertIn("lite", result.summary["routes"])
        self.assertIn("language", result.cases[0])

    def test_prompt_corpus_failure_returns_nonzero_and_writes_report(self):
        module = load_router_validator()
        with tempfile.TemporaryDirectory() as tmp:
            corpus = Path(tmp) / "ROUTER_PROMPT_CORPUS.json"
            report = Path(tmp) / "ROUTER_TEST_REPORT.md"
            corpus.write_text(
                '{"schema_version":"1.0","scenarios":[{"id":"bad","prompt":"只给我 commit message",'
                '"expected_route_id":"dual_index","expected_token_mode":"Token Saver",'
                '"expected_dual_index":false}]}',
                encoding="utf-8",
            )

            with redirect_stderr(io.StringIO()):
                code = module.run(
                    ROOT / "assets" / "templates" / "ROUTER_CONTRACT.json",
                    corpus_path=corpus,
                    report_path=report,
                )

            report_text = report.read_text(encoding="utf-8")
            result = module.run_corpus(
                module.load_contract(ROOT / "assets" / "templates" / "ROUTER_CONTRACT.json"),
                module.load_corpus(corpus),
            ).summary["confusion_pairs"]

        self.assertEqual(1, code)
        self.assertIn("failed", report_text)
        self.assertIn("bad", report_text)
        self.assertIn("## Summary", report_text)
        self.assertTrue(result)
        self.assertEqual("dual_index -> lite", result[0]["pair"])

    def test_cli_rejects_invalid_json(self):
        module = load_router_validator()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ROUTER_CONTRACT.json"
            path.write_text("{invalid", encoding="utf-8")

            with redirect_stderr(io.StringIO()):
                code = module.run(path)

        self.assertEqual(2, code)


if __name__ == "__main__":
    unittest.main()
