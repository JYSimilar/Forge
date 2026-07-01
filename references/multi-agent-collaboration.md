# Multi-Agent Collaboration

Use this when a task benefits from several role views, task lanes, or review perspectives inside the current agent workflow. Forge remains the project manager; "agents" are bounded roles unless the user manually hands artifacts to other tools.

For one bounded role task, use `single-host-role-protocol.md` instead. Use `manual-handoff-notes.md` only when the user explicitly wants to copy an artifact into another tool.

## When to Use

Use for broad work that crosses responsibilities:

- frontend + backend + tests;
- architecture + implementation + review;
- debugging + integration + documentation;
- user asks for multiple roles, multiple task lanes, multiple review perspectives, or explicit AI team roles.

Do not use for tiny tasks, one-file edits, or when a single bounded work order is enough.

## Core Pattern

1. Audit or summarize the project first when the workspace is existing or unclear.
2. Define the shared goal and acceptance criteria.
3. Choose the smallest useful set of agents.
4. Give each agent a fresh task card with only the context it needs.
5. Store the human-readable index in Markdown and the machine-readable index in JSON.
6. Review outputs in two stages: spec compliance first, quality/risk second.
7. Merge through one coordinator when files or interfaces overlap.

Forge generates plans, task cards, indexes, and acceptance gates. It must not claim to run a model runtime, call Claude/Codex/Cursor from another host, dispatch external agents, or trace host execution.

This borrows the useful Superpowers shape: plan before execution, fresh context per role, evidence before completion, and smallest-capable role context that can safely do the job. Forge should not copy heavy ceremony for small tasks.

## Agent Fields

Each agent must have:

- `id`: stable short id;
- `role`: human-readable responsibility;
- `model`: metadata only, such as current model, user preference, or manual handoff note;
- `goal`: one clear goal;
- `allowed_files`: paths or scopes it may change;
- `forbidden_files`: paths or scopes it must not change;
- `status`: one of `planned`, `ready`, `running`, `blocked`, `needs_review`, `done`, `failed`.

Model names are planning metadata. They do not mean Forge can call that model. Cross-model work is user-managed manual handoff.

## Task Card Shape

Every agent task card should include:

```text
功能目标：
输入：
输出：
状态：
异常情况：
限制：
允许修改：
禁止修改：
完成标准：
验证方式：
```

Use `assets/templates/AGENT_TASK_CARD.md`.

## Indexes

Human index: use `assets/templates/MULTI_AGENT_PLAN.md`.

Machine index: use `assets/templates/AGENT_INDEX.json`; structure is documented in `assets/templates/AGENT_INDEX.schema.json`. Validate before execution:

```bash
python scripts/agent_index_validator.py AGENT_INDEX.json
```

The JSON index should track agents, tasks, dependencies, write locks, status, evidence, and artifacts. It is the shared state; do not rely on chat memory as hidden state.

Use `agent_index_update.py` for safe status changes:

```bash
python scripts/agent_index_update.py AGENT_INDEX.json --type task --id T1 --status done --evidence "tests passed"
```

## Boundary Gates

- Validate paths, JSON, statuses, agent ids, model metadata fields, and file scopes.
- Default to no concurrent writes to the same file or nested path.
- Check task dependencies and ensure task outputs stay inside the assigned agent's allowed scope or a declared shared artifact.
- Use a coordinator/integrator for overlapping interfaces.
- Log status and evidence, not secret values.
- If a role lane fails, change something before retry: add context, split the task, switch role perspective, or ask the user.
- Destructive actions, paid APIs, deployment, publish, delete, or bulk rewrite require user confirmation.

## Output Contract

For multi-agent plans, end with 2-3 next options:

1. smallest safe single-role path;
2. recommended multi-role path;
3. deeper review/Burn Mode path when useful.

Keep Token Saver concise. Only expand into large matrices or full work packages when the user asks or the task is clearly complex.
