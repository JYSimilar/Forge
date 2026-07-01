# Forge Skill

Forge is a skill that helps ordinary people turn vague ideas into real, usable things with AI agents.

As a lightweight project-manager skill, it helps users clarify ideas, scope the first useful version, audit existing projects, plan next steps, delegate bounded tasks to AI agents, verify results, write docs, and prepare handoff or release.

Safe Work Order is Forge's default execution unit for AI work. It keeps each AI task small, low-token, reviewable, and bounded by clear context, limits, acceptance checks, verification evidence, stop conditions, and review gates.

Choose a language:

- [中文文档 / zh](docs/zh/README.md)
- [English docs / en](docs/en/README.md)

Quick commands:

- [中文快速调用 / zh](docs/zh/QUICK_COMMANDS.md)
- [English quick commands / en](docs/en/QUICK_COMMANDS.md)

## Stable Version

Current stable version: **Forge 2.2 - Ordinary People + AI Agents + Shippable Progress**.

## What Forge Does

Forge helps users:

- turn a vague idea into an MVP scope;
- decide what to build first and what to defer;
- audit an existing project before changing it;
- plan safe next steps for AI agents;
- execute one bounded step at a time;
- stop at a review gate instead of pushing forward blindly;
- verify results, summarize risks, and choose the next step;
- prepare docs, handoff, or release materials.

## Core Workflow

```text
Vague Idea / Existing Project / Personal Need
↓
Clarify
↓
Choose the smallest useful version
↓
Plan the next concrete step
↓
Safe Work Order
↓
Bounded Execution
↓
Review Gate
↓
Docs / Handoff / Release
```

## Install

```bash
git clone https://github.com/JYSimilar/Forge.git
cd Forge
git checkout <latest-tag>
```

Current stable example:

```bash
git checkout v2.2
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
