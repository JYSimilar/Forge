import json
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


class DualIndexBuilderTests(unittest.TestCase):
    def test_empty_directory_writes_dual_index(self):
        from scripts import dual_index_builder

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "empty"
            out_dir = Path(tmp) / "out"
            workspace.mkdir()

            with redirect_stdout(io.StringIO()):
                code = dual_index_builder.run(str(workspace), str(out_dir))

            payload = json.loads((out_dir / "forge_index.json").read_text(encoding="utf-8"))
            markdown = (out_dir / "FORGE_INDEX.md").read_text(encoding="utf-8")

        self.assertEqual(0, code)
        self.assertEqual("no_project", payload["status"])
        self.assertIn("FORGE_INDEX.md", payload["artifacts"]["human_index"])
        self.assertIn("forge_index.json", payload["artifacts"]["machine_index"])
        self.assertIn("no_project", markdown)
        self.assertIn("选择项目目录", markdown)

    def test_single_project_uses_same_status_and_project_in_markdown_and_json(self):
        from scripts import dual_index_builder

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "project"
            out_dir = Path(tmp) / "out"
            workspace.mkdir()
            (workspace / "package.json").write_text('{"scripts":{"test":"vitest","dev":"vite"}}', encoding="utf-8")
            (workspace / "README.md").write_text("# Demo\n", encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                code = dual_index_builder.run(str(workspace), str(out_dir))

            payload = json.loads((out_dir / "forge_index.json").read_text(encoding="utf-8"))
            markdown = (out_dir / "FORGE_INDEX.md").read_text(encoding="utf-8")

        self.assertEqual(0, code)
        self.assertEqual("single_project", payload["status"])
        self.assertEqual(".", payload["projects"][0]["path"])
        self.assertIn("状态：single_project", markdown)
        self.assertIn("Path: `.`", markdown)
        self.assertIn("npm test", markdown)

    def test_multiple_projects_requires_target_confirmation(self):
        from scripts import dual_index_builder

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "repo"
            out_dir = Path(tmp) / "out"
            frontend = workspace / "frontend"
            backend = workspace / "backend"
            frontend.mkdir(parents=True)
            backend.mkdir(parents=True)
            (frontend / "package.json").write_text('{"scripts":{"test":"vitest"}}', encoding="utf-8")
            (backend / "pyproject.toml").write_text("[project]\nname='api'\n", encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                code = dual_index_builder.run(str(workspace), str(out_dir))

            payload = json.loads((out_dir / "forge_index.json").read_text(encoding="utf-8"))
            markdown = (out_dir / "FORGE_INDEX.md").read_text(encoding="utf-8")

        self.assertEqual(0, code)
        self.assertEqual("multiple_projects", payload["status"])
        self.assertIn("确认目标项目", markdown)

    def test_valid_agent_index_is_summarized(self):
        from scripts import dual_index_builder

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "project"
            out_dir = Path(tmp) / "out"
            agent_index = Path(tmp) / "AGENT_INDEX.json"
            workspace.mkdir()
            (workspace / "package.json").write_text('{"scripts":{"test":"vitest"}}', encoding="utf-8")
            agent_index.write_text(json.dumps(valid_agent_index()), encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                code = dual_index_builder.run(str(workspace), str(out_dir), agent_index_path=str(agent_index))

            payload = json.loads((out_dir / "forge_index.json").read_text(encoding="utf-8"))
            markdown = (out_dir / "FORGE_INDEX.md").read_text(encoding="utf-8")

        self.assertEqual(0, code)
        self.assertIn("agent_index_valid", payload["statuses"])
        self.assertEqual("planner", payload["agents"][0]["id"])
        self.assertEqual("T1", payload["tasks"][0]["id"])
        self.assertIn("planner", markdown)
        self.assertIn("T1", markdown)

    def test_invalid_agent_index_marks_risk_and_returns_one(self):
        from scripts import dual_index_builder

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "project"
            out_dir = Path(tmp) / "out"
            agent_index = Path(tmp) / "AGENT_INDEX.json"
            workspace.mkdir()
            (workspace / "package.json").write_text('{"scripts":{"test":"vitest"}}', encoding="utf-8")
            agent_index.write_text("{not json", encoding="utf-8")

            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                code = dual_index_builder.run(str(workspace), str(out_dir), agent_index_path=str(agent_index))

            payload = json.loads((out_dir / "forge_index.json").read_text(encoding="utf-8"))
            markdown = (out_dir / "FORGE_INDEX.md").read_text(encoding="utf-8")

        self.assertEqual(1, code)
        self.assertIn("agent_index_invalid", payload["statuses"])
        self.assertTrue(any("Invalid JSON" in risk for risk in payload["risks"]))
        self.assertIn("agent_index_invalid", markdown)

    def test_valid_router_contract_is_summarized(self):
        from scripts import dual_index_builder

        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "project"
            out_dir = Path(tmp) / "out"
            workspace.mkdir()
            (workspace / "package.json").write_text('{"scripts":{"test":"vitest"}}', encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                code = dual_index_builder.run(
                    str(workspace),
                    str(out_dir),
                    router_contract_path=str(root / "assets" / "templates" / "ROUTER_CONTRACT.json"),
                )

            payload = json.loads((out_dir / "forge_index.json").read_text(encoding="utf-8"))
            markdown = (out_dir / "FORGE_INDEX.md").read_text(encoding="utf-8")

        self.assertEqual(0, code)
        self.assertIn("router_contract_valid", payload["statuses"])
        self.assertTrue(any(route["id"] == "dual_index" for route in payload["routes"]))
        self.assertIn("router_contract_valid", markdown)

    def test_field_test_json_is_included_when_provided(self):
        from scripts import dual_index_builder

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "project"
            out_dir = Path(tmp) / "out"
            field_test = Path(tmp) / "field_test.json"
            workspace.mkdir()
            (workspace / "package.json").write_text('{"scripts":{"test":"vitest"}}', encoding="utf-8")
            field_test.write_text(
                json.dumps(
                    {
                        "status": "single_project",
                        "triggered_routes": ["Existing Project Audit", "Field Test Loop"],
                        "friction_points": ["missing docs"],
                        "suggested_improvements": ["write README"],
                    }
                ),
                encoding="utf-8",
            )

            with redirect_stdout(io.StringIO()):
                code = dual_index_builder.run(str(workspace), str(out_dir), field_test_json_path=str(field_test))

            payload = json.loads((out_dir / "forge_index.json").read_text(encoding="utf-8"))

        self.assertEqual(0, code)
        self.assertIn("field_test_json_loaded", payload["statuses"])
        self.assertIn("Field Test Loop", payload["source_routes"])
        self.assertIn("missing docs", payload["risks"])

    def test_report_does_not_leak_env_secret_values(self):
        from scripts import dual_index_builder

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "project"
            out_dir = Path(tmp) / "out"
            workspace.mkdir()
            (workspace / "package.json").write_text('{"scripts":{"start":"vite"}}', encoding="utf-8")
            (workspace / ".env").write_text("OPENAI_API_KEY=sk-secret-value-that-must-not-leak\n", encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                code = dual_index_builder.run(str(workspace), str(out_dir))

            payload_text = (out_dir / "forge_index.json").read_text(encoding="utf-8")
            markdown = (out_dir / "FORGE_INDEX.md").read_text(encoding="utf-8")

        self.assertEqual(0, code)
        self.assertNotIn("sk-secret", payload_text)
        self.assertNotIn("sk-secret", markdown)


def valid_agent_index():
    return {
        "schema_version": "1.0",
        "task_id": "dual-index-demo",
        "status": "planned",
        "agents": [
            {
                "id": "planner",
                "role": "Project Planner",
                "model": "gpt-5-mini",
                "goal": "Create the human plan",
                "allowed_files": ["docs"],
                "forbidden_files": ["src"],
                "status": "planned",
            }
        ],
        "tasks": [
            {
                "id": "T1",
                "title": "Create plan",
                "assigned_agent": "planner",
                "goal": "Create the human-readable plan",
                "input": ["WORKSPACE_SUMMARY.md"],
                "output": ["docs/MULTI_AGENT_PLAN.md"],
                "status": "planned",
                "dependencies": [],
                "acceptance": ["Plan references the machine index"],
            }
        ],
        "write_locks": [{"path": "docs", "owner": "planner"}],
        "artifacts": {
            "human_index": "MULTI_AGENT_PLAN.md",
            "machine_index": "AGENT_INDEX.json",
        },
    }


if __name__ == "__main__":
    unittest.main()
