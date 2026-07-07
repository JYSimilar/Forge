from pathlib import Path
import re
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

    def test_language_specific_user_docs_are_indexed(self):
        root = Path(__file__).resolve().parents[1]
        index = (root / "INDEX.md").read_text(encoding="utf-8")
        readme = (root / "README.md").read_text(encoding="utf-8")
        commands = (root / "QUICK_COMMANDS.md").read_text(encoding="utf-8")
        metadata = (root / "agents" / "openai.yaml").read_text(encoding="utf-8")

        expected_files = [
            root / "docs" / "zh" / "README.md",
            root / "docs" / "zh" / "QUICK_COMMANDS.md",
            root / "docs" / "en" / "README.md",
            root / "docs" / "en" / "QUICK_COMMANDS.md",
        ]
        for path in expected_files:
            self.assertTrue(path.exists(), f"{path} should exist")

        for text in (index, readme, commands, metadata):
            self.assertIn("docs/zh/README.md", text)
            self.assertIn("docs/en/README.md", text)

        self.assertIn("docs/zh/QUICK_COMMANDS.md", commands)
        self.assertIn("docs/en/QUICK_COMMANDS.md", commands)

    def test_public_docs_center_project_manager_positioning(self):
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")
        zh_readme = (root / "docs" / "zh" / "README.md").read_text(encoding="utf-8")
        en_readme = (root / "docs" / "en" / "README.md").read_text(encoding="utf-8")
        skill = (root / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("project-manager skill", readme)
        self.assertIn("项目经理型 skill", zh_readme)
        self.assertIn("project-manager skill", en_readme)
        self.assertIn("ordinary people", readme)
        self.assertIn("普通人", zh_readme)
        self.assertIn("ordinary people", en_readme)
        self.assertIn("real, usable things", readme)
        self.assertIn("真实可用成果", zh_readme)
        self.assertIn("real, usable things", en_readme)
        self.assertIn("Who This Is For", readme)
        self.assertIn("What Forge Is Not", readme)
        self.assertIn("not an automatic multi-agent runtime", readme)
        for text in (readme, en_readme, skill):
            self.assertIn("Safe Work Order", text)
            self.assertIn("default execution unit", text)
        self.assertIn("默认执行单元", zh_readme)

    def test_minimal_usage_example_is_indexed(self):
        root = Path(__file__).resolve().parents[1]
        index = (root / "INDEX.md").read_text(encoding="utf-8")
        readme = (root / "README.md").read_text(encoding="utf-8")
        changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
        example_path = root / "examples" / "meeting-notes-mvp.md"
        self.assertTrue(example_path.exists())

        example = example_path.read_text(encoding="utf-8")
        for phrase in (
            "MVP Scope",
            "Safe Work Order",
            "Acceptance Checks",
            "Verification",
            "Stop Condition",
            "Review Gate",
            "Next Options",
        ):
            self.assertIn(phrase, example)

        for text in (index, readme, changelog):
            self.assertIn("meeting-notes-mvp.md", text)

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

    def test_operational_docs_do_not_reference_removed_work_order_files(self):
        root = Path(__file__).resolve().parents[1]
        paths = [
            root / "SKILL.md",
            root / "INDEX.md",
            root / "README.md",
            root / "QUICK_COMMANDS.md",
            root / "agents" / "openai.yaml",
        ]
        removed_names = [
            "agent-compatible-work-protocol.md",
            "host-adapters.md",
            "HOST_WORK_ORDER.md",
            "Agent-Compatible Work Protocol",
            "Host Adapters",
        ]

        for path in paths:
            text = path.read_text(encoding="utf-8")
            for removed_name in removed_names:
                self.assertNotIn(removed_name, text, f"{path} should not reference removed {removed_name}")

    def test_skill_and_index_reference_paths_exist(self):
        root = Path(__file__).resolve().parents[1]
        docs = [
            root / "SKILL.md",
            root / "INDEX.md",
        ]
        reference_pattern = re.compile(r"`(references/[^`]+?\.md)`|`([A-Z][A-Z0-9_]+\.md)`")
        generated_outputs = {
            "FORGE_DOCTOR_REPORT.md",
        }

        for doc in docs:
            text = doc.read_text(encoding="utf-8")
            for match in reference_pattern.finditer(text):
                reference_path = match.group(1)
                template_name = match.group(2)
                if reference_path:
                    self.assertTrue((root / reference_path).exists(), f"{doc} references missing {reference_path}")
                if template_name:
                    if template_name in generated_outputs:
                        continue
                    template_path = root / "assets" / "templates" / template_name
                    root_path = root / template_name
                    self.assertTrue(
                        template_path.exists() or root_path.exists(),
                        f"{doc} references missing template or root doc {template_name}",
                    )

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
