import json
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ForgeDoctorTests(unittest.TestCase):
    def test_empty_directory_reports_no_project(self):
        from scripts import forge_doctor

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "empty"
            out_dir = Path(tmp) / "doctor"
            workspace.mkdir()

            with redirect_stdout(io.StringIO()):
                code = forge_doctor.run(str(workspace), str(out_dir))

            payload = json.loads((out_dir / "forge_doctor.json").read_text(encoding="utf-8"))
            report = (out_dir / "FORGE_DOCTOR_REPORT.md").read_text(encoding="utf-8")

        self.assertEqual(0, code)
        self.assertEqual("no_project", payload["status"])
        self.assertIn("no_project", payload["statuses"])
        self.assertIn("选择项目目录", report)

    def test_skill_repo_release_mode_collects_validation_evidence(self):
        from scripts import forge_doctor

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "skill"
            out_dir = Path(tmp) / "doctor"
            workspace.mkdir()
            (workspace / "SKILL.md").write_text("---\nname: demo\ndescription: Use when testing.\n---\n", encoding="utf-8")
            (workspace / "tests").mkdir()
            (workspace / "tests" / "test_demo.py").write_text("def test_demo():\n    assert True\n", encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                code = forge_doctor.run(
                    str(workspace),
                    str(out_dir),
                    release=True,
                    router_contract_path=str(ROOT / "assets" / "templates" / "ROUTER_CONTRACT.json"),
                )

            payload = json.loads((out_dir / "forge_doctor.json").read_text(encoding="utf-8"))
            report = (out_dir / "FORGE_DOCTOR_REPORT.md").read_text(encoding="utf-8")

        self.assertEqual(0, code)
        self.assertIn("release_mode", payload["statuses"])
        self.assertIn("router_contract_valid", payload["statuses"])
        self.assertTrue(any("quick_validate.py" in item for item in payload["evidence"]))
        self.assertIn("Release readiness", report)

    def test_multiple_projects_requires_target_confirmation(self):
        from scripts import forge_doctor

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "repo"
            out_dir = Path(tmp) / "doctor"
            (workspace / "frontend").mkdir(parents=True)
            (workspace / "backend").mkdir(parents=True)
            (workspace / "frontend" / "package.json").write_text('{"scripts":{"test":"vitest"}}', encoding="utf-8")
            (workspace / "backend" / "pyproject.toml").write_text("[project]\nname='api'\n", encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                code = forge_doctor.run(str(workspace), str(out_dir))

            payload = json.loads((out_dir / "forge_doctor.json").read_text(encoding="utf-8"))
            report = (out_dir / "FORGE_DOCTOR_REPORT.md").read_text(encoding="utf-8")

        self.assertEqual(0, code)
        self.assertEqual("multiple_projects", payload["status"])
        self.assertIn("确认目标项目", report)

    def test_invalid_optional_indexes_return_warning_failure(self):
        from scripts import forge_doctor

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "project"
            out_dir = Path(tmp) / "doctor"
            agent_index = Path(tmp) / "AGENT_INDEX.json"
            router_contract = Path(tmp) / "ROUTER_CONTRACT.json"
            workspace.mkdir()
            (workspace / "package.json").write_text('{"scripts":{"test":"vitest"}}', encoding="utf-8")
            agent_index.write_text("{not json", encoding="utf-8")
            router_contract.write_text('{"routes":[]}', encoding="utf-8")

            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                code = forge_doctor.run(
                    str(workspace),
                    str(out_dir),
                    agent_index_path=str(agent_index),
                    router_contract_path=str(router_contract),
                )

            payload = json.loads((out_dir / "forge_doctor.json").read_text(encoding="utf-8"))
            report = (out_dir / "FORGE_DOCTOR_REPORT.md").read_text(encoding="utf-8")

        self.assertEqual(1, code)
        self.assertIn("agent_index_invalid", payload["statuses"])
        self.assertIn("router_contract_invalid", payload["statuses"])
        self.assertIn("agent_index_invalid", report)

    def test_report_does_not_leak_env_secret_values(self):
        from scripts import forge_doctor

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "project"
            out_dir = Path(tmp) / "doctor"
            workspace.mkdir()
            (workspace / "package.json").write_text('{"scripts":{"start":"vite"}}', encoding="utf-8")
            (workspace / ".env").write_text("OPENAI_API_KEY=sk-secret-value-that-must-not-leak\n", encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                code = forge_doctor.run(str(workspace), str(out_dir))

            payload_text = (out_dir / "forge_doctor.json").read_text(encoding="utf-8")
            report = (out_dir / "FORGE_DOCTOR_REPORT.md").read_text(encoding="utf-8")

        self.assertEqual(0, code)
        self.assertNotIn("sk-secret", payload_text)
        self.assertNotIn("sk-secret", report)


if __name__ == "__main__":
    unittest.main()
