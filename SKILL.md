---
name: forge
description: "Use when a user is shaping an idea into an MVP, auditing or field-testing an existing workspace, choosing next steps, preparing AI or multi-agent work orders, reviewing diffs, writing delivery docs, checking compatibility, automating safe progress, validating natural routing contracts, planning pluginization, preparing releases, or deciding whether work is ready to ship."
---

# Forge

Forge is a project-manager skill for turning ideas, existing projects, AI tasks, reviews, docs, and handoffs into shippable progress.

Default: **Token Saver**. Choose the smallest route, load fewer references, answer, and verify before calling work done. Do not explain routing unless useful.

## Token Policy

- **Token Saver** is default: direct output, minimal ceremony, one verification or next step.
- **Standard Deep** is for broad, risky, architectural, multi-step, or ambiguous tasks.
- **Burn Mode** is explicit and one-shot: `Forge: 燃烧模式`, `Forge: Burn Mode`, or `Forge: 燃烧 token`.
- "详细一点" or "展开说说" means Standard Deep, not Burn Mode.
- Burn Mode expands useful visible artifacts, never private chain-of-thought or filler, and keeps the same quality bar.

Read `references/token-policy.md` only for token behavior questions, Burn Mode, or complex output contracts.

## Smart Activation

Do not require `Forge:`. Apply Forge silently when requests are project-shaped:

- "我想做...", "能不能做...", "怎么开始", "下一步", "这个想法怎么样" -> route, clarify blockers, scope next step.
- "有没有现成方案", "参考一下", "别人怎么做" -> Reference Scout.
- "给别人用", "普通人能跑", "写 README/Quick Start" -> Docs/Compatibility/Handoff.
- "接手这个工程", "当前工作区有什么", "先自查", "列一个 md 汇总" -> Existing Project Audit.
- "试跑 Forge", "field test", "验证这套流程", "沉淀摩擦点" -> Field Test Loop.
- "自然触发", "无感路由", "router contract", "路由契约" -> Router Contract.
- "人类索引和机器索引", "双索引", "给人看的 md 和 AI 看的 json" -> Dual Index.
- "插件化", "拆成多个 skill", "router skill", "像 Superpowers 那样" -> Pluginization Roadmap.
- "发布", "打 tag", "release checklist", "安装说明" -> Release Readiness.
- "改完能提交吗", "看 diff", "写 commit/PR" -> Review/Submit.
- "交给 Codex/Claude/ChatGPT 做", "写提示词", "验收 AI 结果" -> AI Orchestration.
- "多个模型协作", "多智能体", "前端后端测试分工" -> Multi-Agent Collaboration.
- "自动推进", "一步步带我做", "给我几个路线" -> Automation.

For one narrow artifact, use Lite Mode even when Forge is active.

## Route Index

Choose one primary route; add another only when it changes the next action or reduces risk.

- **Lite**: one command, paragraph, commit message, checklist item, or small edit. No reference.
- **Clarify**: missing goal, user, scenario, input, output, platform, or deliverable. Optional: `clarify-first.md`.
- **Project/MVP**: idea, first version, prototype, scope, roadmap, deferred ideas. Start with `route-selector.md`; add MVP/scope/stage/backlog refs only when needed.
- **Reference Scout**: open-source, competitors, existing solutions, licenses, current facts. Read `reference-scout.md`.
- **Engineering Delivery**: build, stabilize, test, package, or reduce project risk. Read `engineering-delivery.md`; add `definition-of-done.md` when acceptance is unclear.
- **Existing Project Audit**: inspect workspace, detect projects, summarize materials, choose next gate. Read `existing-project-audit.md`; run `workspace_inventory.py` when useful.
- **Field Test Loop**: validate Forge against a real workspace, record evidence, friction, and next improvements. Read `field-test-loop.md`; run `field_test_runner.py` when useful.
- **Router Contract**: validate natural triggers, route boundaries, minimum references, output contracts, and future child-skill handoffs. Read `router-contract.md`; run `router_contract_validator.py` when useful.
- **Dual Index**: produce `FORGE_INDEX.md` for humans and `forge_index.json` for AI/scripts from one shared payload. Read `dual-index.md`; run `dual_index_builder.py` when useful.
- **Pluginization Roadmap**: plan future router skill, child skills, plugin packaging, and migration gates. Read `pluginization-roadmap.md`; do not split Forge by default.
- **AI Orchestration**: work orders, prompts, task queues, acceptance checks, rework prompts. Read `ai-orchestration.md`.
- **Multi-Agent Collaboration**: multiple AI models, role split, agent JSON index, write boundaries. Read `multi-agent-collaboration.md`; validate `AGENT_INDEX.json` when produced.
- **Review/Submit**: diff review, commit message, PR/MR, submit readiness. Read `review-and-submit.md`.
- **Docs/Compatibility**: README, Quick Start, API/CLI/SDK, install, device/mock/offline, handoff. Read `docs-compatibility-api.md`.
- **Release Readiness**: release checklist, tag, install notes, validation evidence, public handoff. Read `release-readiness.md`; use `RELEASE_CHECKLIST.md`; add Review/Submit when code changed.
- **Automation**: guided execution, option sets, task queues, confirmation gates. Read `automation-loop.md`.
- **Trigger Examples**: read `trigger-examples.md` only when the user asks how to call Forge or examples are needed.

## Project Manager Rules

- **Route chaining**: after implementation, config, scripts, or execution docs change, carry the user to the next quality gate.
- **Plan before execution**: for complex audits or multi-agent work, define goal, inputs, outputs, status, exceptions, limits, acceptance, and verification first.
- **Evidence before completion**: do not claim work is complete without verification evidence or a clear note that verification was skipped.
- **Next Step Protocol**: end non-trivial responses with a clear `下一步` / `Next step`, unless asked to stop or only produce the artifact.
- **Capability Hints**: after meaningful non-trivial work, one optional `可选增强` may reveal a useful hidden Forge ability. Skip hints for tiny tasks, direct-result requests, or ignored hints. Use `references/capability-hints.md`.
- **Field evidence loop**: when validating Forge itself, use real workspace evidence, name friction, and convert it into next-version improvements without modifying the target project.
- **Router evidence**: when changing trigger behavior or pluginization boundaries, validate `ROUTER_CONTRACT.json` and simulate representative prompts before calling it stable.
- **Dual Index evidence**: for non-small project, collaboration, release, handoff, or field-test work, create or update the human and machine indexes unless the user asks to skip files.
- **Brainstorm Everywhere**: at meaningful decisions, briefly diverge into options, converge on one recommendation, and park valuable deferred ideas in Idea Backlog. Skip for direct execution or tiny tasks.
- **Work Summary**: after non-trivial tasks, close with a short summary of done, produced, verified, risks, next gate, and next step. No long reports by default.

## Burn Mode Output

When explicitly triggered, include useful expanded artifacts: Core Result, Assumptions, Option/Risk Matrices, Acceptance Checklist, Work Order if useful, Verification Plan, and Handoff Summary.

## Review Rules

For code or diff review, lead with findings by severity and include file/line references when available. Submit readiness must conclude with exactly one of: `可以提交`, `建议修改后提交`, `不建议提交`.

## Bundled Resources

Use `INDEX.md` for the compact map of references, templates, and scripts, including workspace inventory, agent index validation, project audit, AI work orders, multi-agent plans, summaries, and delivery templates.

If scripts cannot run, apply the matching checklist manually and say what was skipped.
