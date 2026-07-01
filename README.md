# Forge Skill

Forge is a project-manager skill for turning vague ideas, messy workspaces, and AI-assisted tasks into shippable progress.

It helps users scope MVPs, audit existing projects, plan engineering work, delegate bounded tasks to AI agents, verify results, write docs, and prepare handoff or release.

Safe Work Order is Forge's default execution unit. Every AI task should have a clear goal, context budget, limits, acceptance checks, verification evidence, stop condition, and review gate.

Choose a language:

- [中文文档 / zh](docs/zh/README.md)
- [English docs / en](docs/en/README.md)

Quick commands:

- [中文快速调用 / zh](docs/zh/QUICK_COMMANDS.md)
- [English quick commands / en](docs/en/QUICK_COMMANDS.md)

## Stable Version

Current stable version: **Forge 2.2 - Project Manager Core + Safe Work Order**.

Install from source:

```bash
git clone https://github.com/JYSimilar/Forge.git
cd Forge
git checkout <latest-tag>
```

Current stable example:

```bash
git checkout v2.2
```

## Flow

```text
Idea / Existing Project / Messy Task
↓
Clarify
↓
Scope / Audit / Plan
↓
Safe Work Order
↓
Bounded Execution
↓
Review Gate
↓
Docs / Handoff / Release
```

## Before / After

Before:

```text
帮我把这个项目优化一下。
```

After Forge turns it into project-managed work:

```text
Goal:
Improve the project without broad rewrites.

Required Context:
- README
- package/script manifest
- current failing behavior or user complaint

Do Not Load:
- unrelated generated files
- large build output

Limits:
- no unrelated refactor
- no new heavy dependency without approval

Acceptance Checks:
- identified risk is fixed or clearly scoped
- existing behavior is not regressed

Verification:
- run the smallest relevant test or manual check

Stop Condition:
- stop after one bounded improvement

Review Gate:
- summarize changes, evidence, risks, and next options
```

Forge is the project manager. Safe Work Order is the execution unit it uses when AI work needs clear boundaries.

## Advanced Internals

Advanced routes such as Dual Index, Router Contract, Forge Doctor, Field Test, and multi-role collaboration are documented in [INDEX.md](INDEX.md). Normal users do not need to learn those names first.
