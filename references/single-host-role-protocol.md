# Single-Host Role Protocol

Use this when Forge prepares work for the current installed agent and needs project-manager structure: role views, task cards, acceptance criteria, context budgets, and verification gates.

Forge assumes one current host agent by default. It must not imply Codex can call Claude, Claude can call Codex, or a skill can automatically dispatch work across products or models.

## Boundary

Forge does not call models, dispatch agents, trace host actions, provide memory/RAG, or execute a multi-agent runtime. It creates task protocols the current agent can follow. Cross-tool or cross-model use is manual: the user copies an artifact to another tool if they choose.

## Protocol Shape

Every non-trivial role work order should define:

```text
Current Agent Context:
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

- Use one bounded work order when the current agent can do the job.
- Use Multi-Agent Collaboration only when the user needs multiple roles, task lanes, or review perspectives inside the current agent workflow.
- Use Manual Handoff Notes when the user explicitly wants to copy the result into another tool.
- If the user asks for automatic cross-model or cross-product dispatch, clarify the boundary and offer a manual handoff artifact.
- Use Context Budget Contract when the user mentions token usage, too much context, fewer references, or keeping prompts compact.

## Acceptance First

Define acceptance before execution. The current agent should not mark work complete without evidence such as tests, commands, screenshots, diff review, or a clear “not verified” note.

## Useful Artifacts

Prefer artifacts that remain readable and manually portable without claiming runtime integration:

- `ROLE_WORK_ORDER.md`
- `AI_TASK_BRIEF.md`
- `AGENT_WORK_ORDER.md`
- `AGENT_TASK_CARD.md`
- `ACCEPTANCE_CHECK.md`
- `FORGE_INDEX.md`
- `forge_index.json`

Keep outputs concise by default. Expand only when the task is complex or the user explicitly asks.
