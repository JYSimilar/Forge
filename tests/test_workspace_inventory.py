import json
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
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

    def test_root_project_with_child_workspaces_reports_multiple_projects(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            apps = root / "apps" / "web"
            packages = root / "packages" / "core"
            apps.mkdir(parents=True)
            packages.mkdir(parents=True)
            (root / "package.json").write_text('{"workspaces":["apps/*","packages/*"],"scripts":{"test":"turbo test"}}', encoding="utf-8")
            (apps / "package.json").write_text('{"scripts":{"dev":"vite","test":"vitest"}}', encoding="utf-8")
            (packages / "package.json").write_text('{"scripts":{"build":"tsc"}}', encoding="utf-8")

            result = workspace_inventory.scan_workspace(root)
            paths = {project["path"] for project in result["projects"]}

        self.assertEqual(result["status"], "multiple_projects")
        self.assertIn(".", paths)
        self.assertIn("apps/web", paths)
        self.assertIn("packages/core", paths)

    def test_command_hints_include_package_makefile_and_docker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            root.mkdir()
            (root / "package.json").write_text('{"scripts":{"dev":"vite","test":"vitest"}}', encoding="utf-8")
            (root / "Makefile").write_text("test:\n\tpytest\nrun:\n\tpython app.py\n", encoding="utf-8")
            (root / "Dockerfile").write_text("FROM python:3.12\n", encoding="utf-8")

            project = workspace_inventory.scan_workspace(root)["projects"][0]

        self.assertIn("npm run dev", project["run_commands"])
        self.assertIn("npm test", project["test_commands"])
        self.assertIn("make test", project["test_commands"])
        self.assertIn("docker build -t project .", project["run_commands"])

    def test_python_tests_without_manifest_infer_unittest_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "tests").mkdir()
            (root / "README.md").write_text("# Python Tool\n", encoding="utf-8")
            (root / "scripts" / "tool.py").write_text("def run():\n    return True\n", encoding="utf-8")
            (root / "tests" / "test_tool.py").write_text("def test_tool():\n    assert True\n", encoding="utf-8")

            project = workspace_inventory.scan_workspace(root)["projects"][0]

        self.assertIn("python3 -m unittest discover -s tests -v", project["test_commands"])

    def test_skill_repo_reports_skill_signals_and_validation_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "SKILL.md").write_text("---\nname: demo\ndescription: Use when testing.\n---\n", encoding="utf-8")
            (root / "agents").mkdir()
            (root / "agents" / "openai.yaml").write_text("interface:\n  display_name: Demo\n", encoding="utf-8")
            (root / "references").mkdir()
            (root / "assets" / "templates").mkdir(parents=True)
            (root / "scripts").mkdir()
            (root / "tests").mkdir()
            (root / "tests" / "test_demo.py").write_text("def test_demo():\n    assert True\n", encoding="utf-8")

            project = workspace_inventory.scan_workspace(root)["projects"][0]

        self.assertEqual(project["project_type"], "skill")
        self.assertIn("SKILL.md", project["skill_signals"])
        self.assertIn("agents/openai.yaml", project["skill_signals"])
        self.assertIn("python3 .../quick_validate.py .", project["validation_commands"])
        self.assertIn("python3 -m unittest discover -s tests -v", project["test_commands"])

    def test_invalid_max_files_returns_input_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            with redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
                code = workspace_inventory.run(tmp, max_files=0)

        self.assertEqual(code, 2)

    def test_log_records_skipped_dirs_and_scan_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            root.mkdir()
            (root / "package.json").write_text('{"scripts":{"test":"vitest"}}', encoding="utf-8")
            (root / "node_modules").mkdir()
            (root / "a.js").write_text("console.log(1)\n", encoding="utf-8")
            (root / "b.js").write_text("console.log(2)\n", encoding="utf-8")
            log_path = Path(tmp) / "scan.log"

            with redirect_stdout(io.StringIO()):
                code = workspace_inventory.run(str(root), log_path=str(log_path), max_files=1)
            log_text = log_path.read_text(encoding="utf-8")

        self.assertEqual(code, 0)
        self.assertIn("skipped_dir=node_modules", log_text)
        self.assertIn("file_limit_reached=1", log_text)

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
