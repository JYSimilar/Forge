from pathlib import Path
import unittest


class ReleaseDocsTests(unittest.TestCase):
    def test_pluginization_and_release_templates_are_indexed(self):
        root = Path(__file__).resolve().parents[1]
        index = (root / "INDEX.md").read_text(encoding="utf-8")

        self.assertTrue((root / "references" / "pluginization-roadmap.md").exists())
        self.assertTrue((root / "references" / "release-readiness.md").exists())
        self.assertTrue((root / "references" / "dual-index.md").exists())
        self.assertTrue((root / "assets" / "templates" / "PLUGINIZATION_PLAN.md").exists())
        self.assertTrue((root / "assets" / "templates" / "RELEASE_CHECKLIST.md").exists())
        self.assertTrue((root / "assets" / "templates" / "FORGE_INDEX.md").exists())
        self.assertTrue((root / "assets" / "templates" / "forge_index.json").exists())
        self.assertTrue((root / "scripts" / "dual_index_builder.py").exists())
        self.assertIn("pluginization-roadmap.md", index)
        self.assertIn("release-readiness.md", index)
        self.assertIn("dual-index.md", index)
        self.assertIn("PLUGINIZATION_PLAN.md", index)
        self.assertIn("RELEASE_CHECKLIST.md", index)
        self.assertIn("FORGE_INDEX.md", index)
        self.assertIn("forge_index.json", index)
        self.assertIn("dual_index_builder.py", index)

    def test_stable_core_docs_and_scripts_are_indexed(self):
        root = Path(__file__).resolve().parents[1]
        index = (root / "INDEX.md").read_text(encoding="utf-8")
        readme = (root / "README.md").read_text(encoding="utf-8")
        commands = (root / "QUICK_COMMANDS.md").read_text(encoding="utf-8")
        changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")

        self.assertTrue((root / "references" / "stability-gate.md").exists())
        self.assertTrue((root / "assets" / "templates" / "ROUTER_PROMPT_CORPUS.json").exists())
        self.assertTrue((root / "scripts" / "forge_doctor.py").exists())
        self.assertTrue((root / "scripts" / "forge_index_update.py").exists())
        for text in (index, readme, commands, changelog):
            self.assertIn("Forge 2.0", text)
        self.assertIn("stability-gate.md", index)
        self.assertIn("forge_doctor.py", index)
        self.assertIn("forge_index_update.py", index)
        self.assertNotIn("Forge 1.8 保留", readme)
        self.assertNotIn("Forge 1.8 仍然", readme)


if __name__ == "__main__":
    unittest.main()
