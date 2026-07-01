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
            self.assertIn("Forge 2.2", text)
        self.assertIn("stability-gate.md", index)
        self.assertIn("forge_doctor.py", index)
        self.assertIn("forge_index_update.py", index)
        self.assertNotIn("Forge 1.8 保留", readme)
        self.assertNotIn("Forge 1.8 仍然", readme)

    def test_single_host_role_protocol_docs_and_templates_are_indexed(self):
        root = Path(__file__).resolve().parents[1]
        index = (root / "INDEX.md").read_text(encoding="utf-8")
        readme = (root / "README.md").read_text(encoding="utf-8")
        commands = (root / "QUICK_COMMANDS.md").read_text(encoding="utf-8")
        changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")

        expected_files = [
            root / "references" / "single-host-role-protocol.md",
            root / "references" / "manual-handoff-notes.md",
            root / "references" / "context-budget-contract.md",
            root / "assets" / "templates" / "ROLE_WORK_ORDER.md",
        ]
        for path in expected_files:
            self.assertTrue(path.exists(), f"{path} should exist")
        for text in (index, readme, commands, changelog):
            self.assertIn("Forge 2.2", text)
        self.assertIn("single-host-role-protocol.md", index)
        self.assertIn("manual-handoff-notes.md", index)
        self.assertIn("context-budget-contract.md", index)
        self.assertIn("ROLE_WORK_ORDER.md", index)

    def test_role_templates_do_not_claim_runtime_control(self):
        root = Path(__file__).resolve().parents[1]
        paths = [
            root / "assets" / "templates" / "AI_TASK_BRIEF.md",
            root / "assets" / "templates" / "AGENT_WORK_ORDER.md",
            root / "assets" / "templates" / "AGENT_TASK_CARD.md",
            root / "assets" / "templates" / "ROLE_WORK_ORDER.md",
        ]
        forbidden = [
            "Forge 直接调用模型",
            "Forge 自动调度模型",
            "Forge automatically calls models",
            "Forge dispatches agents automatically",
            "Forge can call Claude",
            "Forge calls Codex",
            "automatically dispatches models",
            "Codex 调 Claude",
            "Claude 调 Codex",
            "Target Host",
        ]
        required = ["Current Agent Context", "Context Budget", "Acceptance First", "Do Not"]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for phrase in required:
                self.assertIn(phrase, text, f"{path} should include {phrase}")
            for phrase in forbidden:
                self.assertNotIn(phrase, text, f"{path} should not claim runtime control")


if __name__ == "__main__":
    unittest.main()
