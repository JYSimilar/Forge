import json
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from scripts import agent_index_update
from tests.test_agent_index_validator import valid_index


class AgentIndexUpdateTests(unittest.TestCase):
    def test_updates_task_status_evidence_and_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "AGENT_INDEX.json"
            path.write_text(json.dumps(valid_index()), encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                code = agent_index_update.run(
                    str(path),
                    target_type="task",
                    target_id="T1",
                    status="done",
                    evidence="unit tests passed",
                    artifact="tests/output.txt",
                )
            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(code, 0)
        self.assertEqual(payload["tasks"][0]["status"], "done")
        self.assertIn("unit tests passed", payload["tasks"][0]["evidence"])
        self.assertIn("tests/output.txt", payload["tasks"][0]["artifacts"])

    def test_invalid_status_does_not_modify_file(self):
        original = valid_index()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "AGENT_INDEX.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with redirect_stderr(io.StringIO()):
                code = agent_index_update.run(
                    str(path),
                    target_type="agent",
                    target_id="frontend",
                    status="finished",
                )
            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(code, 2)
        self.assertEqual(payload["agents"][0]["status"], "planned")


if __name__ == "__main__":
    unittest.main()
