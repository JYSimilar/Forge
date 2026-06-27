# Multi-Agent Collaboration Workflow

Use this when one project goal naturally splits across roles such as frontend, backend, testing, integration, documentation, or review.

## User call

```text
Forge: 让前端、后端、测试几个 AI 分工协作。我想自己定义每个智能体用什么模型，并给我人类看的 md 和 AI 看的 json。
```

## Forge behavior

1. Audit or summarize the workspace first if the project is existing.
2. Create `MULTI_AGENT_PLAN.md` for humans.
3. Create `AGENT_INDEX.json` for agents.
4. Validate the index before execution.
5. Update task or agent status only through a clear status update.

## Useful commands

```bash
python scripts/agent_index_validator.py AGENT_INDEX.json
python scripts/agent_index_update.py AGENT_INDEX.json --type task --id T1 --status done --evidence "unit tests passed" --artifact "tests/output.txt"
```

## Guardrails

- One agent should not write outside its allowed paths.
- Agents should not share hidden state in chat; update Markdown/JSON.
- If an agent fails, change context, split the task, upgrade the model, or ask the user.
- Destructive actions, deployment, publishing, or paid API use require confirmation.
