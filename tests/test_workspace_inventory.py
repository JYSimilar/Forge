import json
import tempfile
import unittest
from pathlib import Path

from scripts import workspace_inventory


class WorkspaceInventoryTests(unittest.TestCase):
    def test_empty_directory_reports_no_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = workspace_inventory.scan_workspace(Path(tmp))

        self.assertEqual(result["status"], "no_project")
        self.assertEqual(result["projects"], [])
        self.assertTrue(result["next_options"])

    def test_single_python_project_is_summarized(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "pyproject.toml").write_text("[project]\nname = 'demo'\n", encoding="utf-8")
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "tests").mkdir()
            (root / "tests" / "test_demo.py").write_text("def test_demo():\n    assert True\n", encoding="utf-8")

            result = workspace_inventory.scan_workspace(root)

        self.assertEqual(result["status"], "single_project")
        self.assertEqual(result["projects"][0]["project_type"], "python")
        self.assertIn("pyproject.toml", result["projects"][0]["manifests"])
        self.assertIn("README.md", result["projects"][0]["docs"])
        self.assertIn("tests", result["projects"][0]["test_indicators"])

    def test_multiple_child_projects_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            frontend = root / "frontend"
            backend = root / "backend"
            frontend.mkdir()
            backend.mkdir()
            (frontend / "package.json").write_text('{"scripts":{"test":"vitest"}}', encoding="utf-8")
            (backend / "pyproject.toml").write_text("[project]\nname = 'api'\n", encoding="utf-8")

            result = workspace_inventory.scan_workspace(root)

        self.assertEqual(result["status"], "multiple_projects")
        self.assertEqual(len(result["projects"]), 2)

    def test_writes_markdown_json_and_redacted_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            out = Path(tmp) / "out"
            root.mkdir()
            out.mkdir()
            (root / "package.json").write_text('{"scripts":{"start":"vite"}}', encoding="utf-8")
            (root / ".env").write_text("OPENAI_API_KEY=sk-secret-value-that-must-not-leak\n", encoding="utf-8")
            md_path = out / "WORKSPACE_SUMMARY.md"
            json_path = out / "workspace.json"
            log_path = out / "scan.log"

            code = workspace_inventory.run(
                str(root),
                markdown_path=str(md_path),
                json_path=str(json_path),
                log_path=str(log_path),
            )

            payload = json.loads(json_path.read_text(encoding="utf-8"))
            log_text = log_path.read_text(encoding="utf-8")
            md_exists = md_path.exists()

        self.assertEqual(code, 0)
        self.assertTrue(md_exists)
        self.assertEqual(payload["status"], "single_project")
        self.assertNotIn("sk-secret", log_text)
        self.assertIn("status=single_project", log_text)


if __name__ == "__main__":
    unittest.main()
