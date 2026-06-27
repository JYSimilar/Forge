# Trigger Examples

Read this only when the user asks how to call Forge, wants examples, or trigger behavior is unclear.

## Token Modes

- "只给我一个 commit message。" -> Token Saver / Lite.
- "这个项目下一步该干嘛？" -> Token Saver route selector.
- "详细一点。" -> Standard Deep, not Burn Mode.
- "Forge: 燃烧模式，帮我拆 MVP。" -> Burn Mode one-shot.
- "Forge: Burn Mode, prepare this for Codex." -> Burn Mode AI work order.

## Chinese Calls

- "做的时候顺便提示我有哪些可选增强能力，但不要一次列太多。" -> Capability Hints.
- "我不知道 Forge 还能帮我做什么，给我一个最相关的可选增强就行。" -> Capability Hints.
- "如果适合找参考、定义完成标准、复盘或交给 Codex，就轻量提醒我。" -> Capability Hints.
- "不要推荐可选能力，只给主流程。" -> skip Capability Hints.

- "做完每一步后，直接告诉我下一步该干什么。" -> Next Step Protocol.
- "给我 3 个下一步选项，都不满意我再补充约束。" -> Next Step Protocol + Option Handling.
- "这一步做完后，是该 review、验收还是交付？" -> Next Step Protocol + Route Chaining.

- "先别写代码，先帮我多想几个方案。" -> brainstorm then recommend.
- "帮我把这些想法收束成第一版能做的功能。" -> Project/MVP.
- "这些想法先记下来，后面版本再考虑。" -> Idea Backlog.
- "第一版先砍掉这些，但告诉我什么时候再做。" -> Scope Control + Idea Backlog.
- "这个 demo 已经能跑了，帮我稳步迭代成更稳定的项目。" -> Engineering Delivery.
- "接手这个工程前，先帮我自查当前工作区。" -> Existing Project Audit.
- "根据当前已有资料列一个 md 汇总。" -> Existing Project Audit + Workspace Summary.
- "如果这里有多个项目，先帮我识别出来。" -> Existing Project Audit.
- "帮我看这次改动能不能提交。" -> Review/Submit.
- "帮我写一份别人也能看懂的 README。" -> Docs/Compatibility.
- "帮我检查 Windows、Mac、Linux、Docker 都怎么跑。" -> Compatibility.
- "把这个目标拆成 AI 可以执行的任务包。" -> AI Orchestration.
- "让前端、后端、测试几个 AI 分工协作。" -> Multi-Agent Collaboration.
- "我想自己定义每个智能体用什么模型。" -> Multi-Agent Collaboration.
- "给我一个人类看的协作计划和 AI 看的 JSON 索引。" -> Multi-Agent Collaboration.
- "AI 做完了，帮我验收一下，不合格就给返工提示词。" -> Acceptance + Rework.
- "我想自动完成这个目标，先给我几个可选路线。" -> Automation.

## Calls Without Saying Forge

- "下一步呢？" -> Next Step Protocol + Route Selector.
- "做完以后该干嘛？" -> Next Step Protocol.

- "我想做一个自动整理笔记的小工具。" -> Clarify + Project/MVP.
- "这个想法别人是不是已经做过了？" -> Reference Scout.
- "这个 demo 给朋友用会不会翻车？" -> Docs/Compatibility + risk.
- "这个文件夹里有什么项目？" -> Existing Project Audit.
- "帮我写一段给 Codex 的任务。" -> AI Orchestration.
- "这个任务要几个 AI 分工比较好？" -> Multi-Agent Collaboration.
- "AI 改完了，你帮我看看行不行。" -> Review/Submit or Acceptance.
- "我想让这件事自动推进。" -> Automation with confirmation gates.

## English Calls

- "turn this idea into a first version" -> Project/MVP.
- "review my changes" -> Review/Submit.
- "prepare this for submit" -> Review/Submit.
- "write docs for real users" -> Docs/Compatibility.
- "find the biggest project risks" -> Engineering Delivery or Review.
