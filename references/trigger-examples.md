# Trigger Examples

Read this only when the user asks how to call Forge, wants examples, or trigger behavior is unclear.

## Token Modes

- "只给我一个 commit message。" -> Token Saver / Lite.
- "这个项目下一步该干嘛？" -> Token Saver route selector.
- "详细一点。" -> Standard Deep, not Burn Mode.
- "Forge: 燃烧模式，帮我拆 MVP。" -> Burn Mode one-shot.
- "Forge: Burn Mode, prepare a current-agent work order." -> Burn Mode AI work order.

## Chinese Calls

- "做的时候顺便提示我有哪些可选增强能力，但不要一次列太多。" -> Capability Hints.
- "我不知道 Forge 还能帮我做什么，给我一个最相关的可选增强就行。" -> Capability Hints.
- "如果适合找参考、定义完成标准、复盘或生成任务单，就轻量提醒我。" -> Capability Hints.
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
- "这个仓库像 monorepo 吗？识别 root、apps 和 packages。" -> Existing Project Audit.
- "用这个真实项目试跑一下 Forge 的自查流程，并记录摩擦点。" -> Field Test Loop.
- "跑一轮 field test，输出 FIELD_TEST_REPORT 和 field_test.json。" -> Field Test Loop.
- "验证这套多智能体规划在当前项目上会不会卡住。" -> Field Test Loop + Multi-Agent Collaboration.
- "把这轮使用 Forge 的问题沉淀成下一版改进建议。" -> Field Test Loop.
- "对这个 Skill 仓库跑一轮 field test，检查 quick_validate、测试命令和发布风险。" -> Field Test Loop + Release Readiness.
- "检查这些自然调用会不会路由到正确能力。" -> Router Contract.
- "先别拆 skill，先校验 router-contract.md 和子能力边界。" -> Router Contract + Pluginization Roadmap.
- "用 ROUTER_CONTRACT.json 模拟这个仓库有什么问题应该走哪条路线。" -> Router Contract.
- "给我一份 ROUTER_TEST_REPORT，记录预期路线、实际路线和修复建议。" -> Router Contract.
- "给我同时生成人类索引和机器索引。" -> Dual Index.
- "输出给人看的 md 和 AI 看的 json，后续协作都以它为准。" -> Dual Index.
- "根据当前工作区生成 FORGE_INDEX.md 和 forge_index.json。" -> Dual Index + Existing Project Audit.
- "不要生成索引文件，只给我结果。" -> skip Dual Index.
- "跑一轮 Forge Doctor 稳定性总检，检查 2.0 稳定版能不能发布。" -> Stability Gate + Release Readiness.
- "更新 forge_index.json 的验证证据，并重新渲染 FORGE_INDEX.md。" -> Dual Index update.
- "用 ROUTER_PROMPT_CORPUS 批量检查自然触发有没有漂移。" -> Router Contract regression.
- "先不要拆实现，帮我设计 router skill + 子 skill 的插件化路线图。" -> Pluginization Roadmap.
- "像 Superpowers 那样拆成多个能力时，哪些应该是子 skill？" -> Pluginization Roadmap.
- "按 RELEASE_CHECKLIST 检查这版能不能打 tag 发布。" -> Release Readiness.
- "帮我整理 GitHub 安装说明、版本 tag、验证命令和已知风险。" -> Release Readiness.
- "帮我看这次改动能不能提交。" -> Review/Submit.
- "帮我写一份别人也能看懂的 README。" -> Docs/Compatibility.
- "帮我检查 Windows、Mac、Linux、Docker 都怎么跑。" -> Compatibility.
- "把这个目标拆成 AI 可以执行的任务包。" -> AI Orchestration.
- "在当前 agent 里按前端、后端、测试几个角色分工。" -> Multi-Agent Collaboration.
- "我想给每个角色记录模型偏好，但不让 Forge 自动调用模型。" -> Multi-Agent Collaboration.
- "给我一个人类看的协作计划和 AI 看的 JSON 索引。" -> Multi-Agent Collaboration.
- "把 AGENT_INDEX 里的 T1 标成 done，并记录验证证据。" -> Multi-Agent Collaboration status update.
- "在当前 agent 里生成一个角色任务单。" -> Single-Host Role Protocol.
- "给当前 Codex 执行的 work order。" -> Single-Host Role Protocol.
- "不要多角色，生成一个通用 agent 任务单。" -> Single-Host Role Protocol.
- "手动复制给 Claude Code 的任务单。" -> Manual Handoff Notes.
- "让 Codex 调 Claude 做 review。" -> Boundary Clarification + Manual Handoff Notes.
- "自动让几个模型并行做。" -> Boundary Clarification + Multi-Agent Collaboration only as role planning.
- "这个任务怎么控制上下文？" -> Context Budget Contract.
- "给我一个低消耗任务单，只包含必要上下文。" -> Context Budget Contract + Single-Host Role Protocol.
- "AI 做完了，帮我验收一下，不合格就给返工提示词。" -> Acceptance + Rework.
- "我想自动完成这个目标，先给我几个可选路线。" -> Automation.

## Calls Without Saying Forge

- "下一步呢？" -> Next Step Protocol + Route Selector.
- "做完以后该干嘛？" -> Next Step Protocol.

- "我想做一个自动整理笔记的小工具。" -> Clarify + Project/MVP.
- "这个想法别人是不是已经做过了？" -> Reference Scout.
- "这个 demo 给朋友用会不会翻车？" -> Docs/Compatibility + risk.
- "这个文件夹里有什么项目？" -> Existing Project Audit.
- "这套 Forge 流程在这个项目上好不好用？" -> Field Test Loop.
- "这个自然触发会不会走错能力？" -> Router Contract.
- "这轮要不要留一个给人和 AI 都能看的索引？" -> Dual Index.
- "这版需要一次稳定性总检。" -> Stability Gate.
- "这个 skill 能不能以后拆成插件？" -> Pluginization Roadmap.
- "这版能不能发布？" -> Release Readiness.
- "帮我写一段当前 agent 可执行的任务。" -> AI Orchestration.
- "这个任务要怎么手动复制给 Claude Code 或 Codex？" -> Manual Handoff Notes + Single-Host Role Protocol.
- "这个任务别加载太多上下文。" -> Context Budget Contract.
- "这个任务要几个 AI 分工比较好？" -> Multi-Agent Collaboration.
- "AI 改完了，你帮我看看行不行。" -> Review/Submit or Acceptance.
- "我想让这件事自动推进。" -> Automation with confirmation gates.

## English Calls

- "turn this idea into a first version" -> Project/MVP.
- "review my changes" -> Review/Submit.
- "prepare this for submit" -> Review/Submit.
- "write docs for real users" -> Docs/Compatibility.
- "find the biggest project risks" -> Engineering Delivery or Review.
- "run a field test on this workspace" -> Field Test Loop.
- "validate the router contract" -> Router Contract.
- "create a human index and machine index" -> Dual Index.
- "run Forge Doctor stable-core checks" -> Stability Gate.
- "create a current-agent role work order" -> Single-Host Role Protocol.
- "prepare a manual handoff note for Claude Code" -> Manual Handoff Notes.
- "keep the task context budget small" -> Context Budget Contract.
- "plan a future plugin split" -> Pluginization Roadmap.
- "prepare this release" -> Release Readiness.
