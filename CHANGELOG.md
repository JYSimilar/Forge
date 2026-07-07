# Changelog

## v2.2 - Project Manager Core + Safe Work Order

- Added language-specific user docs: `docs/zh` for pure Chinese and `docs/en` for pure English.
- Changed the root README into a compact language selector that indexes `zh` and `en`.
- Added regression checks so operational docs cannot point to removed references/templates such as old host-adapter work-order files.
- Clarified Forge as a project-manager skill for helping ordinary people turn vague ideas into usable outcomes with AI agents,
  with Safe Work Order as the default bounded execution unit.
- Re-centered public docs on Forge as a project-manager skill, with Safe Work Order as the default bounded execution unit rather than the whole product.
- Clarified that Safe Work Order is an execution unit inside Forge's broader project-manager workflow.
- Added README audience/non-goal sections and `examples/meeting-notes-mvp.md` for product polish.
- Forge 2.2 turns user feedback about token over-consumption into a Safe Work Order posture: small-step execution, Context Budget, Stop Condition, and Review Gate.
- Added field feedback to README so version evolution is grounded in real usage friction.
- Fixed misleading cross-model wording by making the current installed agent the default execution boundary.
- Reframed Forge work orders around current-agent role protocols instead of cross-host compatibility.
- Replaced host adapter language with manual handoff notes for user-managed copying to other tools.
- Renamed `HOST_WORK_ORDER.md` to `ROLE_WORK_ORDER.md` and replaced `Target Host` with `Current Agent Context`.
- Clarified that multi-agent planning means multi-role/task-lane planning by default; `model` remains metadata, not a callable runtime.
- Added route/test guardrails for cross-model requests such as “Codex 调 Claude” and automatic model dispatch.

## v2.1 - Agent-Compatible Work Protocol

- Added host-agent compatible work protocol references for Claude Code, Codex, Cursor, and generic agents.
- Added `HOST_WORK_ORDER.md` and upgraded AI task templates with Target Host, Context Budget, Acceptance First, and Do Not fields.
- Added context budget and host adapter routing without adding a model runtime, tracing layer, or automatic agent dispatcher.
- Updated router contract, prompt corpus, docs, quick commands, INDEX, and metadata for Forge 2.1.
- Added tests to guard against misleading claims that Forge directly calls or automatically dispatches models.

## v2.0 - Stable Core

- Added `references/stability-gate.md` and `forge_doctor.py` for Forge Doctor stable-core self-checks.
- Added `forge_index_update.py` so `forge_index.json` can be safely updated while re-rendering `FORGE_INDEX.md` from the same payload.
- Added `ROUTER_PROMPT_CORPUS.json` plus router corpus validation and Markdown report output.
- Updated SKILL, INDEX, README, QUICK_COMMANDS, trigger examples, router contract, and OpenAI metadata for Forge 2.0.
- Added unit tests for Forge Doctor, Forge Index updates, router corpus regression, secret redaction, invalid optional indexes, and 2.0 docs coverage.

## v1.9 - Dual Index

- Added `references/dual-index.md` for generating paired human and machine indexes on non-small project work.
- Added `FORGE_INDEX.md` and `forge_index.json` templates.
- Added `dual_index_builder.py` to build both indexes from one shared payload, reusing workspace inventory and optional agent/router/field-test inputs.
- Added Dual Index routing to SKILL, INDEX, README, QUICK_COMMANDS, trigger examples, and router contract.
- Added unit tests for empty, single-project, multi-project, valid/invalid agent index, router contract, field-test JSON, and secret redaction scenarios.

## v1.8 - Router Contract and Pluginization Readiness

- Added `references/router-contract.md` for validating natural triggers, route boundaries, minimum references, completion evidence, and child-skill handoffs.
- Added machine-readable `ROUTER_CONTRACT.json`, human template `ROUTER_CONTRACT.md`, and `ROUTER_TEST_REPORT.md`.
- Added `router_contract_validator.py` to validate the contract and simulate natural prompt routing without model calls.
- Added `references/release-readiness.md` so release/tag requests start from a release-specific gate instead of generic review docs.
- Updated SKILL routing, INDEX, README, QUICK_COMMANDS, trigger examples, pluginization roadmap, and OpenAI metadata for Forge 1.8.
- Added router contract unit tests so future pluginization changes remain verifiable.

## v1.7 - Field-Test Feedback and Release Readiness

- Used Forge 1.6 field-test evidence to improve `workspace_inventory.py`.
- Added Python unittest command inference for codebases with `tests/` but no Python manifest, such as skill repositories.
- Added a regression test for manifest-free Python projects so field tests no longer report missing test commands for this case.
- Added Skill repository detection signals and `validation_commands` so Forge can surface `quick_validate.py` as a validation path.
- Updated Field Test reporting so Skill repositories with validation commands are not treated like normal apps missing run commands.
- Added a pluginization roadmap and template for a future router skill + child skills / plugin architecture.
- Added a release checklist template and README/QUICK_COMMANDS guidance for GitHub install, tags, release readiness, and 1.7 field-test calls.

## v1.6 - Field Test Loop

- Added a repository `.gitignore` for local archives, macOS files, Python caches, logs, and root-level generated Forge artifacts.
- Added `references/field-test-loop.md` and `FIELD_TEST_REPORT.md` for validating Forge against real workspaces.
- Added `field_test_runner.py` to run read-only workspace field tests, write Markdown/JSON reports, and optionally validate `AGENT_INDEX.json`.
- Added unit tests for empty workspaces, single projects, multiple projects, invalid inputs, invalid agent indexes, and secret redaction.
- Updated SKILL routing, INDEX, README, QUICK_COMMANDS, trigger examples, and OpenAI metadata for Forge 1.6.

## v1.5.1 - Audit and Agent Index Hardening

- Improved workspace inventory for monorepo/root-plus-child project detection, run/test command hints, max-file input validation, skipped directory notes, and scan-limit logging.
- Added `AGENT_INDEX.schema.json` and stricter agent index validation for task dependencies, allowed/forbidden scope conflicts, and task outputs outside assigned agent scopes.
- Added `agent_index_update.py` for safe status/evidence/artifact updates using atomic JSON writes.
- Added workflow examples for existing-project audit and multi-agent collaboration.
- Updated README, QUICK_COMMANDS, INDEX, and references for the new hardening behavior.

## v1.5 - Existing Project Audit and Multi-Agent Collaboration

- Added `references/existing-project-audit.md` for detecting existing workspaces, generating workspace summaries, and choosing next quality gates.
- Added `references/multi-agent-collaboration.md` for lightweight multi-agent role planning, model fields, task cards, JSON indexes, write boundaries, and review loops.
- Added `workspace_inventory.py` and `agent_index_validator.py` with unit tests for project detection, sanitized logs, JSON validation, and overlapping write-scope checks.
- Added templates for `WORKSPACE_SUMMARY.md`, `MULTI_AGENT_PLAN.md`, `AGENT_INDEX.json`, and `AGENT_TASK_CARD.md`.
- Integrated the new routes with SKILL routing, Route Selector, AI Orchestration, trigger examples, README, QUICK_COMMANDS, INDEX, and OpenAI metadata.

## v1.4 - Capability Hints

- Added `references/capability-hints.md` for soft recommendations that reveal useful Forge abilities without forcing them into the main workflow.
- Integrated hints with Route Selector, Next Step Protocol, Work Summary, README, QUICK_COMMANDS, trigger examples, and INDEX.
- Added guardrails: at most one hint in Token Saver, skip tiny tasks, do not repeat ignored hints, and do not turn required quality gates into optional suggestions.

## v1.3 - Next Step Protocol

- Added `references/next-step-protocol.md` so Forge ends non-trivial work with a clear next step.
- Added option-handling rules: when the path is unclear, Forge gives 2-3 choices and asks for new constraints if none fit.
- Integrated next-step guidance with Route Selector, Work Summary, Route Chaining, README, QUICK_COMMANDS, trigger examples, and INDEX.
- Clarified that small tasks can skip next-step hints when the user asks for only the result.

## v1.2 - Route Chaining Quality Gates

- Added route chaining rules so Forge does not rely on users knowing the hidden project workflow.
- Engineering Delivery now carries users to the Review/Submit gate after implementation changes.
- Work Summary now includes a `Next gate` field for non-trivial work.
- Added guidance for AI Orchestration acceptance checks, Automation verification, and Docs/Handoff follow-up gates.
- Updated README, QUICK_COMMANDS, route selector, engineering delivery, review, and work summary guidance.

## v1.1 - Idea Backlog

- Added `references/idea-backlog.md` for parking useful ideas deferred from the current version.
- Added `assets/templates/IDEA_BACKLOG.md` to track deferred ideas, revisit triggers, target versions, priority, effort, risk, and status.
- Integrated Idea Backlog with Brainstorm Everywhere, MVP scope control, route selection, Project State, Version Plan, and Work Summary.
- Updated `state_initializer.py` to optionally initialize `IDEA_BACKLOG.md` with other long-running project templates.
- Added quick commands and README guidance for recording and revisiting deferred ideas.

## v1.0 - Stable Release

- Finalized Forge as a project-manager style skill for MVP scoping, AI orchestration, review, docs, automation, handoff, and delivery.
- Made Token Saver the default Forge posture: smaller answers, fewer loaded references, silent routing, and Lite Mode for narrow tasks.
- Added `references/token-policy.md` with Token Saver, Standard Deep, and explicit one-shot Burn Mode rules.
- Added Burn Mode commands: `Forge: 燃烧模式`, `Forge: Burn Mode`, and `Forge: 燃烧 token`.
- Clarified that Burn Mode expands visible artifacts without changing the core recommendation, quality bar, acceptance standard, or risk conclusion.
- Added lightweight Work Summary mechanism.
- Added Boss Report for milestone/project-manager style reporting.
- Added templates for WORK_SUMMARY and BOSS_REPORT.
- Integrated reporting behavior with Token Policy and Lite Mode.
- Updated README, QUICK_COMMANDS, route selector, natural calls, and OpenAI metadata for formal 1.0 use.

## v0.9.2 - Token Policy Modes

- Made Token Saver the default Forge posture: smaller answers, fewer loaded references, silent routing, and Lite Mode for narrow tasks.
- Added `references/token-policy.md` with Token Saver, Standard Deep, and explicit one-shot Burn Mode rules.
- Added Burn Mode commands: `Forge: 燃烧模式`, `Forge: Burn Mode`, and `Forge: 燃烧 token`.
- Clarified that Burn Mode expands visible artifacts without changing the core recommendation, quality bar, acceptance standard, or risk conclusion.
- Updated README, QUICK_COMMANDS, route selector, natural calls, and OpenAI metadata for token-saving defaults.

## v0.9.1 - Smart Activation and Codex Placement

- Fixed `SKILL.md` frontmatter quoting so skill validation passes.
- Added implicit activation rules for project-shaped requests that do not mention `Forge:`.
- Added natural trigger examples for MVP scoping, next-step triage, docs, AI work orders, acceptance checks, and automation.
- Added Codex / OpenAI Agent placement guidance in README.
- Updated OpenAI agent default prompt to match Forge's project-manager and smart-routing role.

## v0.9.0 - AI Project Manager and Simplified Routing

- Added `references/ai-orchestration.md` for AI task delegation, work orders, acceptance checks, and rework prompts.
- Added templates: `AI_TASK_BRIEF.md`, `AGENT_WORK_ORDER.md`, `ACCEPTANCE_CHECK.md`, `REWORK_PROMPT.md`, and `EXECUTION_LOG.md`.
- Upgraded `TASK_QUEUE.md` with role, executor, acceptance criteria, evidence, and rework status fields.
- Added `examples/ai_orchestration_workflow.md`.
- Simplified routing in `SKILL.md` with clear Lite / Clarify / Project / Orchestration / Review / Docs / Automation routes.
- Added natural calls and quick commands for managing AI executors.

## v0.8.0 - Controlled Automation Loop

- Added `references/automation-loop.md` for goal automation, option-first execution, autonomy levels, checkpoints, and confirmation gates.
- Added `AUTOMATION_PLAN.md`, `OPTION_SET.md`, and `TASK_QUEUE.md` templates.
- Added `scripts/automation_initializer.py` to initialize automation planning files.
- Updated `SKILL.md`, `README.md`, `QUICK_COMMANDS.md`, and trigger examples with automation calls and routing.

## v0.7.0 - Lite Mode and Examples

- Added Lite Mode for small concrete tasks.
- Added `examples/` workflows for AI note tools, diff review, non-technical users, and controlled automation.
- Standardized script help behavior across helper scripts.
- Reduced automation task status false positives by using `Pending` instead of the old task placeholder.

## v0.6.0 - Methodology Layer

- Added Stage Gates to identify project phase and next gate.
- Added Definition of Done rules for ideas, MVPs, prototypes, code, docs, APIs, compatibility, submit readiness, and handoff.
- Added Clarify First, Scope Control, Evidence Discipline, Route Selector, and Multi-role Review references.
- Added PROJECT_STATE, DECISION_LOG, RETROSPECTIVE, and PROJECT_HANDOFF templates.
- Added optional `scripts/state_initializer.py` to initialize long-running project templates.
- Updated README, QUICK_COMMANDS, SKILL router, and natural calls for the project methodology workflow.

## v0.4 - Reference Scout

- Added Reference Scout for open-source, competitor, existing-solution, and product-design research.
- Added natural calls for reference scouting and competitor matrix workflows.
- Added evidence fields to reference reports: Source / URL, Last Checked, Evidence, License Source, Confidence.
- Added templates for reference reports, competitor matrices, and candidate scoring CSV.
- Added `reference_ranker.py` for ranking candidate references by fit, speed, docs, maintenance, license friendliness, compatibility, extensibility, and risk.
- Improved `project_audit.py` to avoid false-positive local-path warnings from its own regex definitions.

## v0.3 - Packaging and Audit Improvements

- Cleaned macOS zip artifacts.
- Improved non-Git handling in `diff_review_helper.py`.
- Added warnings for common cache, dependency, and build directories.
- Added clearer installation notes for Claude and Claude Code.

## v0.2 - Forge Workflow

- Added natural-language Forge calls.
- Added brainstorm-everywhere rules.
- Added engineering delivery, review, documentation, compatibility, and API workflows.

## v0.1 - Initial Skill

- Added core project delivery flow: idea -> MVP -> prototype -> test -> review -> docs -> ship.
