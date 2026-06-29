# Forge Compact Index

Use this file when you need one compact map of Forge routes, references, templates, and scripts.

| Route | Minimum Reference | Optional Reference | Useful Templates | Useful Scripts |
|---|---|---|---|---|
| Lite | none | `route-selector.md` | any single requested template | none |
| Clarify | `clarify-first.md` | `brainstorm-to-mvp.md` | `brainstorm_canvas.md`, `OPTION_SET.md` | `idea_ranker.py` |
| Project/MVP | `route-selector.md` | `brainstorm-to-mvp.md`, `scope-control.md`, `stage-gates.md`, `idea-backlog.md` | `mvp_plan.md`, `version_plan.md`, `PROJECT_STATE.md`, `IDEA_BACKLOG.md` | `new_project_scaffold.py` |
| Reference Scout | `reference-scout.md` | `evidence-discipline.md` | `reference_candidates.csv`, `reference_scout_report.md`, `competitor_matrix.md` | `reference_ranker.py` |
| Existing Project Audit | `existing-project-audit.md` | `engineering-delivery.md`, `definition-of-done.md` | `WORKSPACE_SUMMARY.md`, `PROJECT_STATE.md`, `TASK_QUEUE.md` | `workspace_inventory.py`, `project_audit.py` |
| Field Test Loop | `field-test-loop.md` | `existing-project-audit.md`, `multi-agent-collaboration.md` | `FIELD_TEST_REPORT.md`, `WORKSPACE_SUMMARY.md` | `field_test_runner.py`, `workspace_inventory.py`, `agent_index_validator.py` |
| Router Contract | `router-contract.md` | `pluginization-roadmap.md`, `trigger-examples.md` | `ROUTER_CONTRACT.json`, `ROUTER_CONTRACT.md`, `ROUTER_TEST_REPORT.md` | `router_contract_validator.py` |
| Dual Index | `dual-index.md` | `existing-project-audit.md`, `multi-agent-collaboration.md`, `field-test-loop.md` | `FORGE_INDEX.md`, `forge_index.json` | `dual_index_builder.py`, `workspace_inventory.py`, `agent_index_validator.py`, `router_contract_validator.py` |
| Pluginization Roadmap | `pluginization-roadmap.md` | `router-contract.md`, `ai-orchestration.md` | `PLUGINIZATION_PLAN.md`, `ROUTER_CONTRACT.json`, `ROUTER_TEST_REPORT.md` | `router_contract_validator.py` |
| Engineering Delivery | `engineering-delivery.md` | `definition-of-done.md`, then Review/Submit gate | `ACCEPTANCE_CHECK.md`, `EXECUTION_LOG.md`, `troubleshooting.md` | `project_audit.py` |
| AI Orchestration | `ai-orchestration.md` | `definition-of-done.md`, `multi-agent-collaboration.md` | `AI_TASK_BRIEF.md`, `AGENT_WORK_ORDER.md`, `TASK_QUEUE.md`, `REWORK_PROMPT.md` | none |
| Multi-Agent Collaboration | `multi-agent-collaboration.md` | `ai-orchestration.md`, `existing-project-audit.md` | `MULTI_AGENT_PLAN.md`, `AGENT_INDEX.json`, `AGENT_INDEX.schema.json`, `AGENT_TASK_CARD.md`, `ACCEPTANCE_CHECK.md` | `agent_index_validator.py`, `agent_index_update.py`, `workspace_inventory.py` |
| Review/Submit | `review-and-submit.md` | `multi-role-review.md` | `mr_description.md`, `ACCEPTANCE_CHECK.md` | `diff_review_helper.py` |
| Docs/Compatibility | `docs-compatibility-api.md` | `definition-of-done.md` | `quickstart.md`, `api_doc.md`, `troubleshooting.md`, `PROJECT_HANDOFF.md` | `doc_index_builder.py` |
| Release Readiness | `release-readiness.md` | `review-and-submit.md`, `docs-compatibility-api.md`, `field-test-loop.md` | `RELEASE_CHECKLIST.md`, `PROJECT_HANDOFF.md`, `BOSS_REPORT.md` | `field_test_runner.py`, `router_contract_validator.py` |
| Automation | `automation-loop.md` | `stage-gates.md` | `AUTOMATION_PLAN.md`, `OPTION_SET.md`, `TASK_QUEUE.md` | `automation_initializer.py` |
| Work Summary | `work-summary.md` | none | `WORK_SUMMARY.md`, `BOSS_REPORT.md`, `daily_report.md` | `state_initializer.py` |
| Next Step | `next-step-protocol.md` | `route-selector.md`, `work-summary.md` | any current route artifact | none |
| Capability Hints | `capability-hints.md` | `route-selector.md`, `next-step-protocol.md`, `work-summary.md` | current route artifact | none |

## Template One-Liners

- `ACCEPTANCE_CHECK.md`: verify whether an AI/user change meets explicit acceptance criteria.
- `AGENT_WORK_ORDER.md`: hand a bounded coding/task order to another AI agent.
- `AGENT_INDEX.json`: machine-readable multi-agent index with agents, tasks, status, and write locks.
- `AGENT_INDEX.schema.json`: schema reference for the machine-readable multi-agent index.
- `AGENT_TASK_CARD.md`: bounded task card for one AI executor.
- `AI_TASK_BRIEF.md`: split a goal into a compact AI task package.
- `AUTOMATION_PLAN.md`: plan guided or confirmation-gated automation.
- `BOSS_REPORT.md`: summarize progress for a manager or stakeholder.
- `DECISION_LOG.md`: record technical/product decisions and trade-offs.
- `EXECUTION_LOG.md`: record what was done and how it was verified.
- `FIELD_TEST_REPORT.md`: record a real-workspace Forge field test, friction points, evidence, and next improvements.
- `FORGE_INDEX.md`: human-readable index for project status, routes, artifacts, risks, evidence, and next options.
- `IDEA_BACKLOG.md`: park useful ideas deferred from the current version and define when to revisit them.
- `MULTI_AGENT_PLAN.md`: human-readable plan for multi-agent collaboration.
- `OPTION_SET.md`: compare options and recommend one.
- `PLUGINIZATION_PLAN.md`: plan a future router skill, child skills, shared artifacts, and migration gates.
- `PROJECT_HANDOFF.md`: prepare another person to run or continue the project.
- `PROJECT_STATE.md`: capture current project status for later continuation.
- `RETROSPECTIVE.md`: review what worked, what failed, and next improvements.
- `RELEASE_CHECKLIST.md`: check validation, packaging, git, tag, release notes, risks, and next steps before publishing.
- `REWORK_PROMPT.md`: ask an AI agent to fix failed acceptance checks.
- `ROUTER_CONTRACT.json`: machine-readable route contract for natural triggers, minimum references, outputs, evidence, and handoffs.
- `ROUTER_CONTRACT.md`: human-readable route contract planning template.
- `ROUTER_TEST_REPORT.md`: record route simulation, expected/actual routes, issues, and fixes.
- `TASK_QUEUE.md`: track planned, active, blocked, and completed tasks.
- `WORK_SUMMARY.md`: produce a concise completion or handoff summary.
- `WORKSPACE_SUMMARY.md`: summarize an existing workspace before iteration.
- `api_doc.md`: document CLI/API/SDK or integration surfaces.
- `brainstorm_canvas.md`: diverge and converge ideas.
- `competitor_matrix.md`: compare competitors or similar products.
- `daily_report.md`: daily work record.
- `mr_description.md`: PR/MR description.
- `mvp_plan.md`: first shippable version scope.
- `quickstart.md`: install, run, verify for real users.
- `reference_scout_report.md`: summarize researched references and evidence.
- `troubleshooting.md`: common failures and fixes.
- `version_plan.md`: staged version roadmap.
- `forge_index.json`: machine-readable sibling to `FORGE_INDEX.md` for AI, scripts, routes, artifacts, evidence, and risks.
