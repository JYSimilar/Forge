import json
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


class ForgeIndexUpdateTests(unittest.TestCase):
    def test_updates_json_and_markdown_from_same_payload(self):
        from scripts import forge_index_update

        with tempfile.TemporaryDirectory() as tmp:
            index_path = Path(tmp) / "forge_index.json"
            markdown_path = Path(tmp) / "FORGE_INDEX.md"
            index_path.write_text(json.dumps(minimal_index_payload()), encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                code = forge_index_update.run(
                    str(index_path),
                    markdown_path=str(markdown_path),
                    status="single_project",
                    evidence="tests passed",
                    risk="release notes need review",
                    artifact="FORGE_DOCTOR_REPORT.md",
                )

            payload = json.loads(index_path.read_text(encoding="utf-8"))
            markdown = markdown_path.read_text(encoding="utf-8")

        self.assertEqual(0, code)
        self.assertEqual("single_project", payload["status"])
        self.assertIn("tests passed", payload["evidence"])
        self.assertIn("release notes need review", payload["risks"])
        self.assertIn("FORGE_DOCTOR_REPORT.md", payload["artifacts"]["additional"])
        self.assertIn("tests passed", markdown)
        self.assertIn("FORGE_DOCTOR_REPORT.md", markdown)

    def test_rejects_invalid_json_without_writing_markdown(self):
        from scripts import forge_index_update

        with tempfile.TemporaryDirectory() as tmp:
            index_path = Path(tmp) / "forge_index.json"
            markdown_path = Path(tmp) / "FORGE_INDEX.md"
            index_path.write_text("{invalid", encoding="utf-8")

            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                code = forge_index_update.run(str(index_path), markdown_path=str(markdown_path), evidence="x")

        self.assertEqual(2, code)
        self.assertFalse(markdown_path.exists())


def minimal_index_payload():
    return {
        "schema_version": "1.0",
        "status": "single_project",
        "statuses": ["single_project"],
        "workspace": "/tmp/demo",
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
        "risks": [],
        "next_options": [{"option": "继续验收", "why": "确认索引和证据一致。"}],
        "limits": {
            "read_only_target_workspace": True,
            "model_calls": "none",
            "single_payload_source": True,
        },
    }


if __name__ == "__main__":
    unittest.main()
