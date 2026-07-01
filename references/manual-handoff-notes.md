# Manual Handoff Notes

Use this only when the user explicitly wants to manually copy a Forge artifact into another tool such as Claude Code, Codex, Cursor, ChatGPT, or a generic agent.

## Principle

Forge adapts the artifact, not the runtime. It does not bridge products, call another model, or manage cross-tool execution. The user performs the handoff.

## Manual Destinations

- **Claude Code**: if the user copies the task there, keep repo scope, acceptance criteria, and stop conditions explicit.
- **Codex**: if the user copies the task there, include files, tests, verification evidence, and git expectations.
- **Cursor**: if the user copies the task there, keep file scope and editor-local implementation instructions explicit.
- **Generic Agent**: use conservative instructions, small context, explicit input/output, and manual verification.

## Handoff Choice

- Use `ROLE_WORK_ORDER.md` when the user wants one copyable role task.
- Use `AGENT_TASK_CARD.md` when one role needs a reusable task card.
- Use `MULTI_AGENT_PLAN.md` and `AGENT_INDEX.json` only for explicit multi-role planning.
- Use Dual Index when future human/AI continuation matters.

## Warnings

Do not say Forge can call Claude, Codex, Cursor, or any external model. Do not duplicate host features such as native subagents, worktrees, tracing, or model routing. Forge defines the project contract; the current environment or the user executes it.
