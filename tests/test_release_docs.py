from pathlib import Path
import unittest


class ReleaseDocsTests(unittest.TestCase):
    def test_pluginization_and_release_templates_are_indexed(self):
        root = Path(__file__).resolve().parents[1]
        index = (root / "INDEX.md").read_text(encoding="utf-8")

        self.assertTrue((root / "references" / "pluginization-roadmap.md").exists())
        self.assertTrue((root / "references" / "release-readiness.md").exists())
        self.assertTrue((root / "assets" / "templates" / "PLUGINIZATION_PLAN.md").exists())
        self.assertTrue((root / "assets" / "templates" / "RELEASE_CHECKLIST.md").exists())
        self.assertIn("pluginization-roadmap.md", index)
        self.assertIn("release-readiness.md", index)
        self.assertIn("PLUGINIZATION_PLAN.md", index)
        self.assertIn("RELEASE_CHECKLIST.md", index)


if __name__ == "__main__":
    unittest.main()
