import json
import io
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


class ForgeDoctorTests(unittest.TestCase):
    def test_execution_command_selection_allows_only_python_unittest(self):
        from scripts import forge_doctor

        commands, skipped = forge_doctor.select_execution_commands(
            [
                {
                    "absolute_path": "/tmp/project",
                    "test_commands": ["python3 -m unittest discover -s tests -v", "npm test"],
                    "validation_commands": ["python3 .../quick_validate.py ."],
                }
            ]
        )

        self.assertEqual(
            [{"cwd": "/tmp/project", "command": "python3 -m unittest discover -s tests -v"}],
            commands,
        )
        self.assertTrue(any("npm test" in item for item in skipped))
        self.assertTrue(any("quick_validate.py" in item for item in skipped))

    def test_execute_records_redacted_evidence_and_nonzero_failure(self):
        from scripts import forge_doctor

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "skill"
            out_dir = Path(tmp) / "doctor"
            workspace.mkdir()
            (workspace / "SKILL.md").write_text("---\nname: demo\ndescription: Use when testing.\n---\n", encoding="utf-8")
            (workspace / "tests").mkdir()
            (workspace / "tests" / "test_demo.py").write_text("def test_demo():\n    assert True\n", encoding="utf-8")

            fake_execution = {
                "status": "failed",
                "commands": [
                    {
                        "command": "python3 -m unittest discover -s tests -v",
                        "cwd": str(workspace),
                        "exit_code": 1,
                        "duration_seconds": 0.1,
                        "stdout": "OPENAI_API_KEY=super-secret-value",
                        "stderr": "failed",
                        "status": "failed",
                    }
                ],
                "skipped": [],
                "limits": {"network": "denied", "target_workspace": "read_only_copy"},
            }
            with patch.object(forge_doctor, "execute_validation_commands", return_value=fake_execution):
                with redirect_stdout(io.StringIO()):
                    code = forge_doctor.run(str(workspace), str(out_dir), execute=True)

            payload = json.loads((out_dir / "forge_doctor.json").read_text(encoding="utf-8"))
            report = (out_dir / "FORGE_DOCTOR_REPORT.md").read_text(encoding="utf-8")

        self.assertEqual(1, code)
        self.assertEqual("failed", payload["execution"]["status"])
        self.assertIn("[REDACTED]", report)
        self.assertNotIn("super-secret-value", report)

    def test_execute_without_allowlisted_commands_is_skipped(self):
        from scripts import forge_doctor

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "project"
            out_dir = Path(tmp) / "doctor"
            workspace.mkdir()
            (workspace / "package.json").write_text('{"scripts":{"test":"vitest"}}', encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                code = forge_doctor.run(str(workspace), str(out_dir), execute=True)

            payload = json.loads((out_dir / "forge_doctor.json").read_text(encoding="utf-8"))

        self.assertEqual(0, code)
        self.assertEqual("skipped", payload["execution"]["status"])
        self.assertTrue(payload["execution"]["skipped"])

    def test_sandbox_permission_denial_is_reported_as_skipped(self):
        from scripts import forge_doctor

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "skill"
            workspace.mkdir()
            (workspace / "tests").mkdir()
            (workspace / "tests" / "test_demo.py").write_text("def test_demo():\n    assert True\n", encoding="utf-8")
            projects = [
                {
                    "absolute_path": str(workspace),
                    "test_commands": ["python3 -m unittest discover -s tests -v"],
                    "validation_commands": [],
                }
            ]
            denied = subprocess.CompletedProcess(
                args=["sandbox-exec"],
                returncode=71,
                stdout="",
                stderr="sandbox-exec: sandbox_apply: Operation not permitted\n",
            )
            with patch.object(forge_doctor.shutil, "which", return_value="/usr/bin/sandbox-exec"), patch.object(
                forge_doctor.subprocess, "run", return_value=denied
            ):
                execution = forge_doctor.execute_validation_commands(projects, 30, 1000)

        self.assertEqual("skipped", execution["status"])
        self.assertEqual([], execution["commands"])
        self.assertTrue(any("sandbox-exec_unavailable" in item for item in execution["skipped"]))

    def test_execution_redaction_handles_lowercase_secret_assignments(self):
        from scripts import forge_doctor

        text = forge_doctor._redact_text("password=plain-value\napi_token=abc123", 1000)

        self.assertNotIn("plain-value", text)
        self.assertNotIn("abc123", text)
        self.assertIn("password=[REDACTED]", text)
        self.assertIn("api_token=[REDACTED]", text)

    def test_execution_copy_failure_is_recorded(self):
        from scripts import forge_doctor

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "skill"
            workspace.mkdir()
            projects = [
                {
                    "absolute_path": str(workspace),
                    "test_commands": ["python3 -m unittest discover -s tests -v"],
                    "validation_commands": [],
                }
            ]
            with patch.object(forge_doctor.shutil, "which", return_value="/usr/bin/sandbox-exec"), patch.object(
                forge_doctor, "_copy_workspace", side_effect=PermissionError("copy denied")
            ):
                execution = forge_doctor.execute_validation_commands(projects, 30, 1000)

        self.assertEqual("failed", execution["status"])
        self.assertEqual("failed", execution["commands"][0]["status"])
        self.assertIn("copy denied", execution["commands"][0]["stderr"])

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
