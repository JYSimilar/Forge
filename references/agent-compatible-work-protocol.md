# Agent-Compatible Work Protocol

Use this when Forge prepares work for Claude Code, Codex, Cursor, ChatGPT, or another host agent. Forge is the project-manager protocol layer, not an agent runtime.

## Boundary

Forge should not claim to call models, dispatch agents, trace host actions, provide memory/RAG, or execute a multi-agent runtime. It should create portable work orders, acceptance checks, indexes, and handoff notes that the current host agent can use.

## Protocol Shape

Every non-trivial host-agent work order should define:

```text
Target Host:
Goal:
Input:
Output:
Context Budget:
Allowed Scope:
Forbidden Scope:
Acceptance First:
Verification:
Risks:
Do Not:
Next Step:
```

## Routing Rules

- Use one bounded work order when one host agent can do the job.
- Use Multi-Agent Collaboration only when the user asks for multiple models/roles or the task naturally crosses ownership boundaries.
- Use Host Adapter Notes when the user asks how Claude Code, Codex, Cursor, or another host should use the artifact.
- Use Context Budget Contract when the user mentions token usage, too much context, fewer references, or keeping prompts compact.

## Acceptance First

Define acceptance before handing off work. A host agent should not mark work complete without evidence such as tests, commands, screenshots, diff review, or a clear “not verified” note.

## Portable Artifacts

Prefer artifacts that work across hosts:

- `HOST_WORK_ORDER.md`
- `AI_TASK_BRIEF.md`
- `AGENT_WORK_ORDER.md`
- `AGENT_TASK_CARD.md`
- `ACCEPTANCE_CHECK.md`
- `FORGE_INDEX.md`
- `forge_index.json`

Keep outputs concise by default. Expand only when the task is complex or the user explicitly asks.
