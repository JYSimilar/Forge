# Host Adapter Notes

Use this when the user asks how Claude Code, Codex, Cursor, or a generic agent should consume Forge work orders.

## Principle

Forge adapts the artifact, not the runtime. Do not claim the host can do something unless the environment proves it.

## Hosts

- **Claude Code**: good fit for bounded repo tasks, subagents when available, and copyable work orders. Put acceptance and stop conditions in the prompt.
- **Codex**: good fit for repo edits, tests, verification evidence, git-aware handoff, and concise implementation tasks.
- **Cursor**: good fit for editor-local implementation and file-focused instructions. Keep file scope explicit.
- **Generic Agent**: use conservative instructions, small context, explicit input/output, and manual verification.

## Handoff Choice

- Use `HOST_WORK_ORDER.md` when the user wants one copyable prompt for a specific host.
- Use `AGENT_TASK_CARD.md` when one role needs a reusable task card.
- Use `MULTI_AGENT_PLAN.md` and `AGENT_INDEX.json` only for explicit multi-agent planning.
- Use Dual Index when future human/AI continuation matters.

## Warnings

Do not duplicate host features such as native subagents, worktrees, tracing, or model routing. Forge should define the project contract and let the host execute it.
