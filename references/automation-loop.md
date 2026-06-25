# Automation Loop

Use this reference when the user wants Forge to help a goal get completed automatically, semi-automatically, repeatedly, or with a guided sequence of choices.

Forge automation is not blind execution. It is a controlled loop:

goal -> assumptions -> options -> user choice -> small action batch -> verification -> next batch -> handoff/record.

## When to Use

Use this flow when the user says things like:

- 帮我自动完成这个目标
- 让这个项目按步骤自己推进
- 给我几个自动化方案，我选一个
- 我不懂技术，你带我一步步做
- 先给选项，不满意我再补充
- 把这个任务拆成可执行队列
- 每完成一步就检查并继续
- 用最低人工成本完成这个项目

Also use it lightly when a broad Forge task has multiple possible routes and the user would benefit from choosing a path.

## Automation Safety Principle

Never treat automation as permission to do irreversible or external actions without confirmation.

Always ask for explicit confirmation before:

- deleting files or data
- overwriting important files
- installing heavy dependencies
- running destructive scripts
- committing, pushing, deploying, publishing, or sending messages
- calling paid APIs or spending money
- using secrets, tokens, credentials, or private data
- changing production configuration
- scraping websites or bypassing access controls
- making legal, financial, medical, or high-stakes decisions

For safe local planning, drafting, scaffolding, and reversible file creation, Forge may proceed after stating assumptions and planned output.

## Autonomy Levels

When automation is requested, first choose an autonomy level or ask the user to choose:

| Level | Name | Use When | Behavior |
|---|---|---|---|
| 0 | Plan only | User only wants strategy | Produce plan, no execution |
| 1 | Guided steps | User is non-technical | One small step at a time, user executes |
| 2 | Prepare assets | User wants files/prompts/docs | Generate drafts/scripts/templates, ask before risky use |
| 3 | Safe local execution | Tool environment supports execution | Run reversible local checks/builds, report results |
| 4 | Confirmation-gated execution | External/destructive actions involved | Pause before each risky action |

Default to Level 1 for ordinary users and Level 2 for project work unless the user explicitly asks for more automation and the environment allows it.

## Option-First Automation

Before executing a non-trivial goal, provide 2-4 options:

1. Fastest path: lowest friction, best for demo.
2. Stable path: slightly slower, better for long-term use.
3. Low-tech path: easier for non-programmers.
4. Extensible path: best if the project may grow.

For each option include:

- What it does
- Time/effort
- What the user needs to provide
- Main risk
- Best fit

Then recommend one option.

If the user rejects all options, ask them to supplement constraints instead of guessing endlessly:

- 哪个点不满意：成本、复杂度、平台、效果、时间、技术栈、隐私、可维护性？
- 有没有必须使用/不能使用的工具？
- 目标是演示、自己用、给别人用，还是长期产品？

Then generate a new option set.

## Goal Contract

For any automated plan, create a small goal contract:

- Goal: what should be true at the end
- User: who it is for
- Deliverable: app / script / doc / API / demo / workflow / report
- Inputs: what information or files are needed
- Constraints: time, platform, tools, budget, privacy, complexity
- Automation level: 0-4
- Definition of Done: how success will be verified
- Stop conditions: when Forge should pause and ask

Do not start broad execution without this contract unless the task is tiny.

## Execution Loop

Use this loop for automation:

1. Clarify only blocking unknowns.
2. Produce 2-4 options and recommend one.
3. After user choice, create an automation plan.
4. Split into small batches of 1-3 actions.
5. For each batch, state expected output and verification.
6. Execute or instruct depending on autonomy level.
7. Verify result.
8. Update task queue and known risks.
9. Continue, adjust, or stop.
10. At completion, generate handoff/retrospective if useful.

## Output Template

When the user asks for automation, use this compact structure:

```text
我理解的目标：
当前假设：
建议自动化等级：

可选方案：
A. 最快方案：...
B. 稳妥方案：...
C. 低技术方案：...
D. 可扩展方案：...

我的推荐：
需要你选择/补充：
下一步我会做：
暂停条件：
```

After the user chooses:

```text
自动化计划：
1. ...
2. ...
3. ...

第一批动作：
- 动作：
- 预期结果：
- 验证方式：
- 是否需要确认：
```

## Human-Friendly Automation

For ordinary users:

- Avoid jargon.
- Give copyable commands only when necessary.
- Explain where files go.
- Provide visible success criteria.
- Show one next step, not twenty.
- Convert technical choices into plain trade-offs.

Example:

Instead of “configure environment variables,” say “把 API key 放到 `.env` 文件里，这样不用写进代码，也不容易泄露。”

## Automation Across Forge Stages

Automation can be used at every Forge stage:

- Clarify: auto-generate key questions and assumptions.
- Scout: auto-generate search keywords, comparison tables, and reference ranking.
- Scope: auto-cut feature lists into must-do/not-do.
- Build: auto-create project skeleton and first runnable loop.
- Stabilize: auto-generate fix queue ordered by risk.
- Review: auto-check diff, docs, tests, compatibility, secrets.
- Document: auto-generate user/developer/deployment docs.
- Ship: auto-create commit/MR/handoff/release notes.
- Reflect: auto-create retrospective and next iteration queue.

Always keep the loop visible so users feel in control.
