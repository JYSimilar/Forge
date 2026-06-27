import json
import io
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

from scripts import agent_index_validator


def valid_index():
    return {
        "schema_version": "1.0",
        "task_id": "forge-demo",
        "status": "planned",
        "agents": [
            {
                "id": "frontend",
                "role": "Frontend Builder",
                "model": "gpt-5-mini",
                "goal": "Build UI shell",
                "allowed_files": ["src/ui"],
                "forbidden_files": ["src/api"],
                "status": "planned",
            },
            {
                "id": "tester",
                "role": "Tester",
                "model": "gpt-5",
                "goal": "Verify behavior",
                "allowed_files": ["tests"],
                "forbidden_files": ["src/ui"],
                "status": "planned",
            },
        ],
        "tasks": [
            {
                "id": "T1",
                "title": "Build UI shell",
                "assigned_agent": "frontend",
                "goal": "Create the main interface",
                "input": ["README.md"],
                "output": ["src/ui/App.tsx"],
                "status": "planned",
                "dependencies": [],
                "acceptance": ["UI renders"],
            }
        ],
        "write_locks": [{"path": "src/ui", "owner": "frontend"}],
    }


class AgentIndexValidatorTests(unittest.TestCase):
    def test_valid_index_passes(self):
        result = agent_index_validator.validate_index(valid_index())

        self.assertEqual(result.errors, [])
        self.assertTrue(result.ok)

    def test_missing_agent_model_fails(self):
        payload = valid_index()
        del payload["agents"][0]["model"]

        result = agent_index_validator.validate_index(payload)

        self.assertFalse(result.ok)
        self.assertTrue(any("agents[0].model" in error for error in result.errors))

    def test_overlapping_write_scopes_fail(self):
        payload = valid_index()
        payload["agents"][1]["allowed_files"] = ["src/ui/components"]

        result = agent_index_validator.validate_index(payload)

        self.assertFalse(result.ok)
        self.assertTrue(any("overlapping write scope" in error for error in result.errors))

    def test_invalid_json_file_returns_error_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "AGENT_INDEX.json"
            path.write_text("{not json", encoding="utf-8")

            with redirect_stderr(io.StringIO()):
                code = agent_index_validator.run(str(path))

        self.assertEqual(code, 2)

    def test_unknown_task_agent_fails(self):
        payload = valid_index()
        payload["tasks"][0]["assigned_agent"] = "missing"

        result = agent_index_validator.validate_index(payload)

        self.assertFalse(result.ok)
        self.assertTrue(any("unknown assigned_agent" in error for error in result.errors))

    def test_unknown_task_dependency_fails(self):
        payload = valid_index()
        payload["tasks"][0]["dependencies"] = ["missing-task"]

        result = agent_index_validator.validate_index(payload)

        self.assertFalse(result.ok)
        self.assertTrue(any("unknown dependency" in error for error in result.errors))

    def test_agent_allowed_and_forbidden_scope_conflict_fails(self):
        payload = valid_index()
        payload["agents"][0]["forbidden_files"] = ["src/ui/components"]

        result = agent_index_validator.validate_index(payload)

        self.assertFalse(result.ok)
        self.assertTrue(any("allowed_files conflicts with forbidden_files" in error for error in result.errors))

    def test_task_output_outside_assigned_scope_fails(self):
        payload = valid_index()
        payload["tasks"][0]["output"] = ["src/api/server.ts"]

        result = agent_index_validator.validate_index(payload)

        self.assertFalse(result.ok)
        self.assertTrue(any("outside allowed scope" in error for error in result.errors))


if __name__ == "__main__":
    unittest.main()
