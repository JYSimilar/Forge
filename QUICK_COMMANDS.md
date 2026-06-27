# Forge 快速调用指令

不用记模式，直接说你想让 Forge 做什么。你也可以完全不说 `Forge:`；只要请求像项目推进、MVP、提交检查、文档、AI 任务或自动化，Forge 就应该自动选择合适能力。

默认省 token：Forge 会优先用 Token Saver，少读资料、少解释模式、直接给结果。只有你显式输入 `Forge: 燃烧模式`、`Forge: Burn Mode` 或 `Forge: 燃烧 token`，才会一次性输出大量矩阵、清单、验收表和交接稿。

## Token 模式

```text
只给我这次提交的 commit message，不用解释。
```

```text
这个项目下一步该干嘛？给我最重要的 3 件事。
```

```text
详细一点，但不用燃烧模式。
```

```text
Forge: 燃烧模式，帮我拆 MVP。
```

```text
Forge: Burn Mode, prepare this task for Codex.
```

```text
Forge: 燃烧 token，帮我做提交前完整验收。
```

## Work Summary / 工作总结 / Boss Report

```text
Forge: 干完这轮后，给我一个简短工作总结。
```

```text
Forge: 总结本轮完成了什么、风险是什么、下一步做什么。
```

```text
Forge: 用项目经理的方式总结这次进展。
```

```text
Forge: 给我一份可以发给负责人看的阶段报告。
```

```text
Forge: write a Boss Report for this milestone.
```

```text
Forge: 这轮不要写报告，直接给结果。
```

## 不说 Forge 也可以

```text
我想做一个自动整理笔记的小工具，第一版怎么开始？
```

```text
这个项目下一步该干嘛？
```

```text
这个 demo 给朋友用会不会翻车？
```

```text
帮我把这件事交给 Codex 做，提示词要边界清楚。
```

```text
AI 改完了，你帮我验收一下。
```

```text
我想让这件事自动推进，先给我几个路线。
```

## Existing Project Audit / 已有工程自查

```text
Forge: 接手这个工程前，先帮我自查当前工作区。
```

```text
Forge: 根据当前已有资料列一个 md 汇总。
```

```text
Forge: 这个文件夹里有没有项目？如果有，告诉我技术栈、风险和下一步。
```

```text
Forge: 如果这里有多个项目，先帮我识别出来，不要直接改文件。
```

```text
Forge: 检查这个项目放生产会不会炸，重点看错误处理、日志、输入校验、并发安全和测试。
```

## Multi-Agent Collaboration / 多智能体协作

```text
Forge: 让前端、后端、测试几个 AI 分工协作，并给我人类看的 md 和 AI 看的 json。
```

```text
Forge: 我想自己定义每个智能体用什么模型，帮我规划任务边界。
```

```text
Forge: 这个任务需要几个 agent？一个负责架构，一个负责实现，一个负责测试校验。
```

```text
Forge: 给每个 agent 输出任务卡，包含功能目标、输入、输出、状态、异常情况和限制。
```

```text
Forge: 多 agent 之前先检查写入范围，避免两个 AI 同时改同一个文件。
```

## 最常用

```text
Forge: 帮我把这个想法变成能跑的第一版。
```

```text
Forge: 帮我从 0 搭这个项目，普通人也能照着做。
```

```text
Forge: 这个 demo 已经能跑了，帮我稳步迭代成更稳定的项目。
```

## Brainstorm Everywhere

```text
Forge: 先别写代码，先帮我多想几个方案。
```

```text
Forge: 这一步给我 3 个方案，然后推荐最适合落地的一个。
```

```text
Forge: 帮我挑刺，看看这个想法哪里不靠谱。
```

```text
Forge: 每一步都先小范围头脑风暴，再收敛成可执行方案。
```

## 延后想法池 / Idea Backlog

```text
Forge: 这些想法第一版先不做，但有价值的帮我记录到后续版本。
```

```text
Forge: 帮我把这次砍掉但以后可能有用的功能整理成 IDEA_BACKLOG。
```

```text
Forge: 重新检查 IDEA_BACKLOG，看看下一版哪些想法值得拿出来做。
```

```text
Forge: 第一版先砍掉这些功能，但告诉我什么时候应该重新考虑。
```

## 开源参考和竞品设计

```text
Forge: 先别写代码，先帮我找开源参考和已有产品设计。
```

```text
Forge: 这个功能有没有现成方案？帮我判断能不能直接用。
```

```text
Forge: 帮我做一个竞品功能矩阵，然后收敛成我的 MVP。
```

```text
Forge: 帮我分析这些 GitHub 项目哪个最适合快速做原型。
```

```text
Forge: 看看同类产品一般怎么设计这个功能，再给我自己的第一版方案。
```

## 原型和迭代

```text
Forge: 帮我拆第一版，只保留最核心功能。
```

```text
Forge: 帮我快速搭一个能演示的原型。
```

```text
Forge: 帮我规划下一步迭代，按优先级来。
```

```text
Forge: 帮我做项目体检，列出最该先修的问题。
```

## AI 项目经理 / 支配 AI 干活

```text
Forge: 把这个目标拆成 AI 可以执行的任务包。
```

```text
Forge: 给 Codex 写一个边界清楚、低消耗的任务提示词。
```

```text
Forge: 这个任务应该交给哪个 AI 角色做？哪些我自己确认？
```

```text
Forge: AI 做完了，帮我按完成标准验收一下，不合格就给返工提示词。
```

```text
Forge: 把这个项目拆成任务队列，标出哪些交给人，哪些交给 ChatGPT / Claude Code / Codex。
```

```text
Forge: 帮我写一份 AGENT_WORK_ORDER，我要直接复制给另一个 AI 执行。
```

## 路由衔接 / 自动质量门

```text
Forge: 实现完成后不要直接结束，自动提醒我下一步该 review、验收还是交付。
```

```text
Forge: 这次代码改完后，自动接一次 Review/Submit 自查。
```

```text
Forge: 不要默认我知道流程，做完每一步都告诉我下一个质量门。
```

## 下一步协议 / Next Step Protocol

```text
Forge: 做完每一步后，直接告诉我下一步该干什么。
```

```text
Forge: 不要默认我懂流程，每次给我一个明确下一步。
```

```text
Forge: 给我 3 个下一步选项；如果都不合适，再问我限制条件。
```

```text
Forge: 这一步做完后，告诉我是该 review、验收、写文档、提交，还是进入下一批任务。
```

```text
Forge: 只给结果，不要下一步提示。
```

## 能力提示 / Capability Hints

```text
Forge: 做的时候顺便提示我有哪些可选增强能力，但不要一次列太多。
```

```text
Forge: 我不知道 Forge 还能帮我做什么，给我一个最相关的可选增强就行。
```

```text
Forge: 如果这一步适合找参考、定义完成标准、复盘或交给 Codex，就轻量提醒我。
```

```text
Forge: 不要推荐可选能力，只给主流程。
```

## 提交前检查

```text
Forge: 帮我看这次改动能不能提交。
```

```text
Forge: 帮我检查 diff，有没有无关改动、本机路径、密钥或临时代码。
```

```text
Forge: 帮我生成 commit message 和 PR 描述。
```

## 文档、接口、兼容

```text
Forge: 帮我写一份别人也能看懂的 README。
```

```text
Forge: 帮我写 Quick Start，要求普通人能照着跑起来。
```

```text
Forge: 帮我设计这个功能对外怎么调用。
```

```text
Forge: 帮我检查 Windows、Mac、Linux、Docker 都怎么跑。
```

## 自动化推进

```text
Forge: 我想自动完成这个目标，先给我几个可选路线，我选一个。
```

```text
Forge: 把这个目标拆成任务队列，每次推进一小步，遇到风险动作先问我。
```

```text
Forge: 给我最快、最稳、最低技术门槛三个方案，不满意我再补充约束。
```

```text
Forge: 我选方案 B，接下来按小批次推进，每批告诉我预期结果和验证方式。
```

```text
Forge: 这些方案我都不满意，重新问我关键约束再给一版。
```

## 轻量模式

```text
Forge: 这个是小任务，直接给我结果和一个验证步骤，不用跑完整流程。
```

```text
Forge: 只帮我改这一段 README，保持简短。
```

```text
Forge: 只给我这次提交的 commit message。
```

## 项目方法论

```text
Forge: 我这个想法还不清楚，先帮我问关键问题。
```

```text
Forge: 帮我判断这个项目现在处于什么阶段，下一步最该做什么。
```

```text
Forge: 帮我给这个任务定义完成标准。
```

```text
Forge: 第一版哪些必须做，哪些明确不做？
```

```text
Forge: 这个方案从产品、工程、文档、风险几个角度帮我审一下。
```

```text
Forge: 帮我生成 PROJECT_STATE，方便后面继续开发。
```

```text
Forge: 帮我记录这次技术选择的决策。
```

```text
Forge: 这一轮做完了，帮我复盘一下。
```

```text
Forge: 我要把项目交给别人，帮我写一份交接文档。
```

## English

```text
forge: brainstorm ideas
forge: turn this idea into a first version
forge: find open-source references
forge: analyze similar products
forge: build a prototype
forge: automate this goal
forge: create an AI task brief
forge: write a Codex work order
forge: acceptance check this AI output
forge: give me options first
forge: review my changes
forge: write docs for real users
forge: check compatibility
```
