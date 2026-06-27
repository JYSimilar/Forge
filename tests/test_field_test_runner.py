import json
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


class FieldTestRunnerTests(unittest.TestCase):
    def test_empty_directory_reports_no_project(self):
        from scripts import field_test_runner

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "empty"
            out_dir = Path(tmp) / "out"
            workspace.mkdir()

            with redirect_stdout(io.StringIO()):
                code = field_test_runner.run(str(workspace), str(out_dir))

            payload = json.loads((out_dir / "field_test.json").read_text(encoding="utf-8"))
            report = (out_dir / "FIELD_TEST_REPORT.md").read_text(encoding="utf-8")

        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "no_project")
        self.assertIn("no_project", payload["statuses"])
        self.assertIn("选择项目目录", report)

    def test_single_project_writes_report_and_json(self):
        from scripts import field_test_runner

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "project"
            out_dir = Path(tmp) / "out"
            workspace.mkdir()
            (workspace / "package.json").write_text('{"scripts":{"test":"vitest","dev":"vite"}}', encoding="utf-8")
            (workspace / "README.md").write_text("# Demo\n", encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                code = field_test_runner.run(str(workspace), str(out_dir))

            payload = json.loads((out_dir / "field_test.json").read_text(encoding="utf-8"))
            report = (out_dir / "FIELD_TEST_REPORT.md").read_text(encoding="utf-8")

        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "single_project")
        self.assertEqual(payload["workspace_inventory"]["projects"][0]["project_type"], "node")
        self.assertIn("FIELD_TEST_REPORT.md", payload["artifacts"])
        self.assertIn("npm test", report)

    def test_multiple_projects_requires_target_confirmation(self):
        from scripts import field_test_runner

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
                code = field_test_runner.run(str(workspace), str(out_dir))

            payload = json.loads((out_dir / "field_test.json").read_text(encoding="utf-8"))
            report = (out_dir / "FIELD_TEST_REPORT.md").read_text(encoding="utf-8")

        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "multiple_projects")
        self.assertIn("确认目标项目", report)

    def test_invalid_workspace_returns_input_error(self):
        from scripts import field_test_runner

        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing"
            out_dir = Path(tmp) / "out"

            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                code = field_test_runner.run(str(missing), str(out_dir))

        self.assertEqual(code, 2)

    def test_invalid_agent_index_is_reported_without_false_success(self):
        from scripts import field_test_runner

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "project"
            out_dir = Path(tmp) / "out"
            agent_index = Path(tmp) / "AGENT_INDEX.json"
            workspace.mkdir()
            (workspace / "package.json").write_text('{"scripts":{"test":"vitest"}}', encoding="utf-8")
            agent_index.write_text("{not json", encoding="utf-8")

            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                code = field_test_runner.run(str(workspace), str(out_dir), agent_index_path=str(agent_index))

            payload = json.loads((out_dir / "field_test.json").read_text(encoding="utf-8"))
            report = (out_dir / "FIELD_TEST_REPORT.md").read_text(encoding="utf-8")

        self.assertEqual(code, 1)
        self.assertIn("agent_index_invalid", payload["statuses"])
        self.assertIn("agent_index_invalid", report)
        self.assertNotIn("agent_index_valid", payload["statuses"])

    def test_report_does_not_leak_env_secret_values(self):
        from scripts import field_test_runner

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "project"
            out_dir = Path(tmp) / "out"
            workspace.mkdir()
            (workspace / "package.json").write_text('{"scripts":{"start":"vite"}}', encoding="utf-8")
            (workspace / ".env").write_text("OPENAI_API_KEY=sk-secret-value-that-must-not-leak\n", encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                code = field_test_runner.run(str(workspace), str(out_dir))

            payload_text = (out_dir / "field_test.json").read_text(encoding="utf-8")
            report = (out_dir / "FIELD_TEST_REPORT.md").read_text(encoding="utf-8")

        self.assertEqual(code, 0)
        self.assertNotIn("sk-secret", payload_text)
        self.assertNotIn("sk-secret", report)


if __name__ == "__main__":
    unittest.main()
