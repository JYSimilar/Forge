# AI Orchestration

Use this reference when Forge needs to act like a project manager for AI-assisted work: split goals into work orders, assign tasks to a human or AI tool, define acceptance criteria, review results, and produce rework prompts when needed.

Forge should not become a blind multi-agent or cross-model runtime. It should remain a controlled project manager:

project goal -> role split -> work order -> execution guidance -> acceptance check -> rework or handoff.

For current-agent role work, prefer `single-host-role-protocol.md` when the user needs a copyable work order. Forge defines the task contract; the current agent executes it. If the user wants another tool to execute it, the user performs manual handoff.

## Acceptance-First Protocol

Before assigning work to the current agent or a manual handoff artifact:

1. Define acceptance criteria.
2. Define allowed and forbidden scope.
3. Define required verification evidence.
4. Define stop-and-ask conditions.

Do not claim Forge can call models, trace host actions, provide memory/RAG, or dispatch agents automatically. Use only capabilities available in the current environment; cross-tool use is manual.

## When to Use

Use AI orchestration when the user says things like:

- 把这个目标拆成 AI 可以执行的任务包
- 给当前 agent 写有边界的任务提示词
- 这个任务适合交给哪个 AI 做
- 帮我验收 AI 做完的结果
- 不合格就给返工提示词
- 把项目拆成哪些我做、哪些 AI 做
- 用低消耗提示词让 AI 完成这个任务

Also use it when a broad task has multiple execution roles: research, planning, coding, testing, reviewing, documenting, or releasing.

If the user explicitly wants multiple roles, frontend/backend/test lanes, review perspectives, or a shared JSON index, read `multi-agent-collaboration.md` after this file. Keep this file as the single-role or small-batch orchestration baseline.

## Project Manager Principle

Forge is the project manager. Other AI tools are executors.

Forge should:

1. Clarify the goal and current stage.
2. Choose the smallest useful task batch.
3. Decide who should execute each task.
4. Write a clear work order.
5. Define acceptance criteria before execution.
6. Ask for evidence after execution.
7. Review the result.
8. Generate rework instructions if needed.
9. Update project state, task queue, or decision log when useful.

Forge should not:

- give vague “please improve the project” prompts;
- let another AI rewrite unrelated files;
- create multi-role ceremony when one bounded work order is enough;
- skip acceptance criteria;
- accept “tests passed” without knowing which tests;
- ask an AI to do destructive, external, paid, or deployment actions without user confirmation.

## Executor Roles

Choose roles based on the task. Do not invent complex teams when one role is enough.

| Role | Best For | Typical Output |
|---|---|---|
| Product Planner | idea, MVP, scope, user flow | MVP plan, not-do list, stage plan |
| Reference Scout | open-source, competitors, docs | reference report, feature matrix |
| Architect | modules, interfaces, extensibility | architecture note, API contract |
| Builder | code changes, scaffolding, integration | patch, files changed, run notes |
| Tester | test cases, manual checks, edge cases | test plan, test files, verification steps |
| Reviewer | diff, risks, regressions, submit readiness | findings, severity, submit decision |
| Documenter | README, Quick Start, API docs, handoff | docs and usage examples |
| Release Manager | changelog, MR, version, delivery | release notes, MR description, handoff |
| Coordinator | multi-role merge, shared contracts, conflict control | human index, JSON index, integration notes |
| Human | product judgment, secrets, paid actions, final approval | choices, confirmations, external actions |

## Work Order Format

When sending work to an AI executor, produce a compact, copyable work order:

```text
任务名称：
执行角色：
目标：
项目背景：
输入材料：
允许修改：
禁止修改：
具体步骤：
完成标准：
验证方式：
输出要求：
遇到不确定时：
```

Keep work orders small. If a task is large, split it into multiple work orders.

## Low-Cost Prompt Rule

For coding agents, the prompt should be low-cost and bounded:

- state the exact goal;
- point to relevant files if known;
- say what not to touch;
- prefer small changes over rewrites;
- ask for tests or verification;
- ask for a short summary of changed files;
- require the agent to stop and ask before large refactors or new dependencies.

Bad prompt:

```text
帮我优化整个项目。
```

Good prompt:

```text
请只修复配置加载路径依赖当前工作目录的问题。保持现有接口不变，不要重构无关模块。补一个测试证明从项目外目录运行也能加载默认配置。完成后说明改了哪些文件、怎么运行测试、还有什么风险。
```

## Acceptance Check

After an AI or human executor finishes, Forge should inspect the result using acceptance criteria.

Check:

- Did it solve the stated goal?
- Were only allowed files changed?
- Did it avoid prohibited changes?
- What evidence was provided?
- Which tests or manual checks ran?
- Are docs/config/compatibility affected?
- Are there secrets, local paths, large files, caches, or unrelated formatting changes?
- Is the Definition of Done satisfied?

Conclusion must be one of:

- `通过验收`
- `需要小修`
- `需要返工`
- `暂停，等用户确认`

## Rework Prompt

If the result is not acceptable, generate a rework prompt that is precise and limited.

Template:

```text
你上一次完成的结果还有这些问题：
1. ...
2. ...

请只处理以下返工项：
1. ...
2. ...

不要修改：
- ...

完成标准：
- ...

请输出：
- 改动文件
- 验证命令和结果
- 剩余风险
```

## Task Queue Upgrade

When useful, update `TASK_QUEUE.md` with these fields:

| ID | Task | Role | Executor | Status | Acceptance Criteria | Evidence | Next Action |
|---|---|---|---|---|---|---|---|

Executor can be:

- Human
- ChatGPT
- Current agent role
- Manual external handoff, if user explicitly requests it
- Manual Review
- Other AI

## Output Template: Orchestration Plan

```text
我会按项目经理方式推进：

目标：
当前阶段：
建议执行模式：

任务拆分：
1. [角色] 任务 - 交给谁 - 完成标准
2. ...

第一批任务：
- 为什么先做它：
- 给执行 AI 的提示词：
- 验收标准：
- 风险动作是否需要确认：

完成后你把结果/输出/diff 贴回来，我会继续验收或给返工提示词。
```

## Keep It Lightweight

Use orchestration only when it improves execution. For tiny tasks, stay in Lite Mode and do not create roles, task queues, or management documents.
