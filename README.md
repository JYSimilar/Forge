# Forge Skill

Forge turns vague work into safe agent work orders.

Choose a language:

- [中文文档 / zh](docs/zh/README.md)
- [English docs / en](docs/en/README.md)

Quick commands:

- [中文快速调用 / zh](docs/zh/QUICK_COMMANDS.md)
- [English quick commands / en](docs/en/QUICK_COMMANDS.md)

## Stable Version

Current stable version: **Forge 2.2 - Safe Work Order**.

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

## What Forge Does

Forge helps an AI agent:

- clarify a vague task;
- create a low-token Safe Work Order;
- define context budget, limits, acceptance, and stop conditions;
- execute one bounded step;
- stop at a review gate;
- verify, summarize, and choose the next step.

## Advanced Internals

Advanced routes such as Dual Index, Router Contract, Forge Doctor, Field Test, and multi-role collaboration are documented in [INDEX.md](INDEX.md). Normal users do not need to learn those names first.
