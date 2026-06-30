# Multi-Agent Collaboration

Use this when a task benefits from several AI executors with separate roles, models, and work boundaries. Forge remains the project manager; agents are executors.

For a single Claude Code, Codex, Cursor, or generic host-agent handoff, use `agent-compatible-work-protocol.md` instead. Multi-agent planning is for explicit multiple roles/models or genuinely separate work streams.

## When to Use

Use for broad work that crosses responsibilities:

- frontend + backend + tests;
- architecture + implementation + review;
- debugging + integration + documentation;
- user asks for multiple models, multiple agents, or explicit AI team roles.

Do not use for tiny tasks, one-file edits, or when a single bounded work order is enough.

## Core Pattern

1. Audit or summarize the project first when the workspace is existing or unclear.
2. Define the shared goal and acceptance criteria.
3. Choose the smallest useful set of agents.
4. Give each agent a fresh task card with only the context it needs.
5. Store the human-readable index in Markdown and the machine-readable index in JSON.
6. Review outputs in two stages: spec compliance first, quality/risk second.
7. Merge through one coordinator when files or interfaces overlap.

Forge generates plans, task cards, indexes, and acceptance gates. It must not claim to run a model runtime, dispatch host subagents, or trace host execution unless the host environment explicitly exposes that capability.

This borrows the useful Superpowers shape: plan before execution, fresh context per agent, evidence before completion, and least-capable model that can safely do the job. Forge should not copy heavy ceremony for small tasks.

## Agent Fields

Each agent must have:

- `id`: stable short id;
- `role`: human-readable responsibility;
- `model`: user-chosen or recommended model name;
- `goal`: one clear goal;
- `allowed_files`: paths or scopes it may change;
- `forbidden_files`: paths or scopes it must not change;
- `status`: one of `planned`, `ready`, `running`, `blocked`, `needs_review`, `done`, `failed`.

Model names are planning metadata. Forge must not claim a host can actually call a model unless the environment proves it.

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

- Validate paths, JSON, statuses, agent ids, model fields, and file scopes.
- Default to no concurrent writes to the same file or nested path.
- Check task dependencies and ensure task outputs stay inside the assigned agent's allowed scope or a declared shared artifact.
- Use a coordinator/integrator for overlapping interfaces.
- Log status and evidence, not secret values.
- If an agent fails, change something before retry: add context, split the task, upgrade model, or ask the user.
- Destructive actions, paid APIs, deployment, publish, delete, or bulk rewrite require user confirmation.

## Output Contract

For multi-agent plans, end with 2-3 next options:

1. smallest safe single-agent path;
2. recommended multi-agent path;
3. deeper review/Burn Mode path when useful.

Keep Token Saver concise. Only expand into large matrices or full work packages when the user asks or the task is clearly complex.
