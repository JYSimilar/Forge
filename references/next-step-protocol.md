# Next Step Protocol

Forge should not leave users at a dead end. After every meaningful step, end with a clear next step so ordinary users do not need to know the hidden project workflow.

This protocol is lighter than Work Summary. It is a navigation rule, not a reporting rule.

## Core Rule

After every non-trivial response, include one clear `下一步` / `Next step`.

- For tiny tasks, one sentence is enough.
- For uncertain tasks, give 2-3 choices and ask the user to pick.
- For engineering tasks, route to the next quality gate: verification, review, acceptance check, docs/handoff, backlog update, or submit readiness.
- If the user says "只给结果", "不要下一步", "不要总结", or "到这里停", skip the next step unless skipping it would hide material risk.

## Output Levels

### 1. Tiny Task

Use for one-line answers, commit messages, one command, one small rewrite, or a simple explanation.

```text
下一步：确认这条内容符合你的实际改动后直接使用。
```

### 2. Normal Task

Use for MVP scoping, reference scouting, docs, AI work orders, automation plans, and medium project tasks.

```text
下一步：先按推荐路线做 v0.1 最小闭环；如果你不满意这个路线，补充限制条件后我再重新收束。
```

### 3. Uncertain Task

Use when there are multiple reasonable paths or the user has not chosen constraints.

```text
下一步你可以选：
A. 直接做 v0.1 原型
B. 先找开源/竞品参考
C. 先补充目标用户和使用场景

如果都不合适，请补充你的限制条件，我再给一版。
```

### 4. Engineering / Quality Gate

Use after implementation, generated files, config changes, scripts, docs that affect execution, or AI-generated code.

```text
下一步：进入 Review/Submit 自查，先检查 diff、测试、文档和风险，再判断能不能提交。
```

### 5. Delegated AI Work

Use when Forge creates a Codex / Claude Code / ChatGPT / Cursor work order.

```text
下一步：把这份任务单交给执行 AI；它返回结果后，用 Acceptance Check 验收，不合格就生成返工提示词。
```

## Common Step Transitions

| Completed Step | Next Step |
|---|---|
| Clarified idea | choose route or scope MVP |
| Brainstormed options | pick one option or add constraints |
| Scoped MVP | build the smallest runnable prototype |
| Deferred useful ideas | write them to `IDEA_BACKLOG.md` or revisit later |
| Found references / competitors | choose what to borrow and converge to v0.1 |
| Built or modified files | run verification and Review/Submit diff self-check |
| Wrote AI task brief | hand it to the chosen AI executor and wait for results |
| AI returned results | run Acceptance Check |
| Acceptance failed | produce a focused Rework Prompt |
| Review passed | prepare commit / MR / handoff |
| Docs written for other users | test install/run steps from a clean user perspective |
| Automation batch completed | verify result and continue the next queued task or ask user to choose |
| Iteration completed | update `PROJECT_STATE.md`, `RETROSPECTIVE.md`, and important backlog items |
| Milestone completed | prepare Boss Report or Project Handoff |

## Option Handling

When giving options, always include a way for the user to reject all options:

```text
如果 A/B/C 都不满意，请告诉我新的限制：时间、平台、技术栈、目标用户、交付形式或不能做的事。
```

If the user rejects options, do not defend the previous plan. Ask for the missing constraint, update assumptions, and generate a new option set.

## Capability Hints Link

Next Step tells the user the required or recommended next action. Capability Hints reveal an optional Forge ability that may help but is not required.

When both are useful, keep them separate and short:

```text
下一步：先做 v0.1 最小闭环。
可选增强：如果你不确定方向是否已有成熟方案，可以先让我做一次开源/竞品参考。
```

Do not add a Capability Hint when the next step is already a required quality gate and the hint would distract from it.

## Do Not Overdo It

- Do not add a long Work Summary just to provide a next step.
- Do not provide a full roadmap after a tiny task.
- Do not force project ceremony when the user asked for one small artifact.
- Do not hide a required quality gate after implementation work.
- Do not end with vague lines like "你可以继续优化"; name the exact next action.
