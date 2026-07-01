# Forge Skill

Forge, 中文可以叫“造物”。

一句话：**Forge = 把模糊任务变成能交给 AI agent 执行的安全任务单，并负责验收、总结和下一步。**

它适合普通用户这样理解：

1. 你说一个想法、需求、项目问题或下一步困惑。
2. Forge 帮你收束目标、拆任务、写清楚边界和验收标准。
3. 当前 agent 按任务单执行，或者你手动复制交接稿给其他工具。
4. 做完后 Forge 帮你验收结果、说明风险、给下一步。

## Version

Forge 2.2 is the Safe Work Order release. The main user-facing flow is: clarify the goal -> create a low-token safe work order -> execute one bounded step -> stop at a review gate -> verify -> summarize -> choose the next step.

它适合这些场景：

- 把一个模糊想法变成能运行的第一版。
- 接手已有工程时，先看清楚项目现状、风险和下一步。
- 给当前 agent 生成安全任务单：目标、输入、输出、限制、验收、验证。
- AI 做完后帮你验收结果，不合格就生成返工提示。
- 检查 diff、准备 commit message 和 PR/MR 描述。
- 写 README、Quick Start、交接文档、发布检查清单。

高级能力也有，但不用一开始理解：双索引、Router Contract、Forge Doctor、Field Test、多角色协作、插件化路线图，都属于进阶项目管理和稳定性工具。

## Why v2.2 / 真实反馈

Field feedback: previous versions reduced lazy stopping, but could over-consume tokens when a user wanted a small, safe next step. Forge 2.2 introduces a stricter Safe Work Order posture:

- default to small-step execution;
- set a clear Context Budget before loading extra material;
- stop at a Review Gate instead of pushing forward indefinitely;
- treat cross-tool work as manual handoff, not automatic model dispatch.

This makes Forge less like a feature tour and more like an AI agent project delivery protocol.

## 推荐调用

可以显式说 Forge：

```text
Forge: 帮我把这个想法变成能跑的第一版。
```

```text
Forge: 这一步给我 3 个方案，然后推荐最适合落地的一个。
```

```text
Forge: 先别写代码，先帮我找开源参考和同类产品设计。
```

```text
Forge: 帮我看这次改动能不能提交。
```

更多可复制调用见 `QUICK_COMMANDS.md`。

也可以不说 Forge。只要请求像项目推进、MVP、原型、AI 任务、diff review、文档、兼容、自动化或交付，Forge 就应该自动选择最小可用流程，例如：

```text
我想做一个自动整理笔记的小工具，第一版怎么开始？
```

```text
这个项目给朋友用还差什么？
```

```text
帮我把这件事写成当前 agent 能执行的任务单，边界要清楚。
```

## 真实使用演示

用户输入：

```text
我想做一个能自动整理会议纪要的小工具，第一版怎么开始？
```

Forge 典型输出会像这样：

```text
功能目标：
把“会议录音/文字记录”整理成结构化纪要，第一版先支持用户粘贴文本，不做录音转写。

第一版范围：
1. 输入会议文字
2. 输出摘要、待办事项、负责人、截止时间
3. 支持复制 Markdown

暂时不做：
- 账号系统
- 多人协作
- 自动录音转写
- 日历/飞书/Slack 集成

给当前 agent 的第一张任务单：
- 目标：搭一个本地可运行的单页原型
- 输入：一段会议文本
- 输出：结构化 Markdown 纪要
- 限制：不接外部 API，不引入复杂后端
- 验收：能用示例文本生成摘要和待办清单
- 验证：运行项目并用一段测试会议文本手动检查输出

风险/限制：
- 纯规则提取可能漏掉隐含负责人或截止时间
- 如果要更聪明，需要后续接入模型 API

下一步：
1. 先做可运行原型
2. 再补 README 和示例输入
3. 最后做一次验收，判断能不能给朋友试用
```

这就是 Forge 的主要价值：不只是回答“可以做”，而是把事情变成当前 agent 能安全执行、能验收、能继续推进的工作包。

## 高级能力 / Advanced

高级功能默认不会打扰小任务。只有项目变复杂、要交付、要多人/多角色协作、要长期维护时才需要它们。

推荐路径：先自查已有工程，再生成或更新双索引，然后用任务/多角色/交付路线推进，最后用 Forge Doctor 做稳定性总检。小任务仍然走 Token Saver，不会默认生成报告或文件。

```text
Forge: 跑一轮 Forge Doctor 稳定性总检，检查这版能不能发布。
```

```text
Forge: 用 ROUTER_PROMPT_CORPUS 批量检查自然触发有没有漂移。
```

```text
Forge: 更新 forge_index.json 的验证证据，并重新渲染 FORGE_INDEX.md。
```

稳定性总检：

```bash
python scripts/forge_doctor.py . --out-dir /private/tmp/forge-doctor --release
```

可选合并现有索引：

```bash
python scripts/forge_doctor.py . --out-dir /private/tmp/forge-doctor --release --agent-index assets/templates/AGENT_INDEX.json --router-contract assets/templates/ROUTER_CONTRACT.json
```

## Forge 2.2 Safe Work Order / 省 token 安全执行

Forge 2.2 的核心是“省 token 的安全任务单”：默认小步执行，先写清上下文预算、允许范围、禁止范围、验收标准和停手条件。它不会声称自己能让 Codex 调 Claude、Claude 调 Codex、自动调度多个模型、做 tracing 或替代宿主 agent 的原生能力。跨工具使用只能是用户手动复制交接稿。

```text
Forge: 在当前 agent 里生成一个角色任务单，要包含验收标准、上下文预算和不要碰的范围。
```

```text
Forge: 给当前 Codex 执行的 work order，只包含必要上下文。
```

```text
Forge: 手动复制给 Claude Code 的任务单，说明这是人工交接。
```

```text
Forge: 这个任务怎么控制上下文，避免读太多 reference？
```

## Existing Project Audit / 已有工程自查

接手已有工程时，Forge 会先看当前工作区有没有项目，再决定下一步。它会识别 manifest、README、测试线索、脚本、技术栈、monorepo/多项目结构、运行/测试命令和明显风险，并能生成 `WORKSPACE_SUMMARY.md`。

```text
Forge: 接手这个工程前，先帮我自查当前工作区。
```

```text
Forge: 根据当前已有资料列一个 md 汇总。
```

辅助脚本：

```bash
python scripts/workspace_inventory.py /path/to/workspace --markdown WORKSPACE_SUMMARY.md --json workspace.json --log workspace_scan.log
```

输出状态会是 `no_project`、`single_project` 或 `multiple_projects`。如果检测到多个项目，Forge 会先让用户确认目标，而不是直接改文件。

## Multi-Agent Collaboration / 多智能体协作

当任务跨前端、后端、测试、调试、文档或 review 时，Forge 可以生成轻量多角色协作计划。默认这些 agent 是当前宿主里的角色视角/任务泳道，不是多个真实模型自动并发执行。模型名只是元数据或人工交接备注，不代表 Forge 能调用模型。

```text
Forge: 在当前 agent 里按前端、后端、测试几个角色分工，并给我人类看的 md 和 AI 看的 json。
```

```text
Forge: 我想给每个角色记录模型偏好，但不让 Forge 自动调用模型，帮我规划任务边界。
```

相关模板：

- `MULTI_AGENT_PLAN.md`：人类看的协作计划。
- `AGENT_INDEX.json`：AI 之间看的机器索引。
- `AGENT_INDEX.schema.json`：机器索引的结构说明。
- `AGENT_TASK_CARD.md`：单个 agent 的任务卡。

校验 JSON 索引：

```bash
python scripts/agent_index_validator.py AGENT_INDEX.json
```

安全更新任务或 agent 状态：

```bash
python scripts/agent_index_update.py AGENT_INDEX.json --type task --id T1 --status done --evidence "unit tests passed"
```

## Field Test Loop / 实战闭环

Forge 保留实战闭环：当你想验证 Forge 这套流程在真实项目上是否好用时，它会只读扫描 workspace，记录触发路线、证据、摩擦点、风险和下一步改进。它不会调用模型，也不会修改目标工程，并会把真实摩擦点转成下一轮小步优化。

```text
Forge: 用这个真实项目试跑一下 Forge 的自查流程，并记录摩擦点。
```

```text
Forge: 跑一轮 field test，看看多智能体规划前还有什么卡点。
```

辅助脚本：

```bash
python scripts/field_test_runner.py /path/to/workspace --out-dir /path/to/out --max-files 2000
```

如果已经有多智能体索引，可以顺便校验：

```bash
python scripts/field_test_runner.py /path/to/workspace --out-dir /path/to/out --agent-index AGENT_INDEX.json
```

Skill 仓库会额外暴露校验线索，例如：

```text
Skill validation: python3 .../quick_validate.py .
Test command: python3 -m unittest discover -s tests -v
```

## Pluginization Roadmap / 插件化路线

Forge 2.2 仍然只设计插件化路线，不实际拆分。未来可以把 Forge 拆成一个轻量 router skill，再拆出 audit、orchestration、review、docs、release、field-test 等子 skill 或 plugin 能力。

```text
Forge: 先不要拆实现，帮我设计 router skill + 子 skill 的插件化路线图。
```

```text
Forge: 用 PLUGINIZATION_PLAN 模板规划未来怎么拆，但这轮不要真的拆。
```

对应文件：

- `references/router-contract.md`
- `assets/templates/ROUTER_CONTRACT.json`
- `references/pluginization-roadmap.md`
- `assets/templates/PLUGINIZATION_PLAN.md`

## Router Contract / 无感路由契约

Forge 不真正拆 skill，但把未来拆分前最容易乱的部分先做成可验证契约：自然触发词、路线 ID、最低读取 reference、默认输出、完成证据和交接路线。

```text
Forge: 检查这些自然调用会不会路由到正确能力。
```

```text
Forge: 先别拆 skill，先校验 router contract 和子能力边界。
```

验证契约：

```bash
python scripts/router_contract_validator.py assets/templates/ROUTER_CONTRACT.json
```

模拟一个自然调用：

```bash
python scripts/router_contract_validator.py assets/templates/ROUTER_CONTRACT.json --simulate "这个仓库有什么问题？"
```

批量回归自然调用：

```bash
python scripts/router_contract_validator.py assets/templates/ROUTER_CONTRACT.json --corpus assets/templates/ROUTER_PROMPT_CORPUS.json --report ROUTER_TEST_REPORT.md
```

它只是本地确定性 smoke test，不会调用模型，也不会改项目。

## Dual Index / 双索引

Forge 2.2 在非小型项目任务中可以生成或更新双索引：`FORGE_INDEX.md` 给人看，`forge_index.json` 给 AI、脚本和后续路由看。两个文件来自同一份 payload，避免 Markdown 和 JSON 各说各话。

```text
Forge: 给我同时生成人类索引和机器索引。
```

```text
Forge: 输出给人看的 md 和 AI 看的 json，后续协作都以它为准。
```

辅助脚本：

```bash
python scripts/dual_index_builder.py /path/to/workspace --out-dir /path/to/out
```

可选合并现有索引：

```bash
python scripts/dual_index_builder.py /path/to/workspace --out-dir /path/to/out --agent-index AGENT_INDEX.json --router-contract ROUTER_CONTRACT.json --field-test-json field_test.json
```

安全追加证据并重渲染 Markdown：

```bash
python scripts/forge_index_update.py forge_index.json --markdown FORGE_INDEX.md --evidence "tests passed" --artifact "FORGE_DOCTOR_REPORT.md"
```

## Token 模式

Forge 默认是 **Token Saver**：自动路由，但少读 reference、少解释模式、少做仪式，优先给直接结果和一个验证/下一步。小任务会走 Lite Mode；复杂、风险高或架构相关任务会自动进入适度展开的 Standard Deep，但仍然控制 token。

只有显式命令才会进入一次性的 **Burn Mode**：

```text
Forge: 燃烧模式，帮我拆 MVP。
```

```text
Forge: Burn Mode, prepare this task for the current agent.
```

```text
Forge: 燃烧 token，帮我做提交前完整验收。
```

Burn Mode 不会提高或降低核心质量；它和默认模式使用同一套路线、完成标准和验收逻辑，只是多输出矩阵、清单、任务单、风险表、验证计划和交接稿。说“详细一点”不会触发 Burn Mode，只会适度展开。

## Idea Backlog / 延后想法池

Forge 在头脑风暴和 MVP 收敛时，不会把所有被砍掉的想法都丢掉。对于“有价值，但当前版本不合适”的想法，可以记录到 `IDEA_BACKLOG.md`，并写清楚为什么现在不做、什么时候重新评估、可能放到哪个版本。

```text
Forge: 这些想法第一版先不做，但有价值的帮我记录到后续版本。
```

```text
Forge: 重新检查 IDEA_BACKLOG，看看下一版哪些想法值得拿出来做。
```

这个机制适合避免两种问题：第一版做太大；好想法被临时砍掉后彻底丢失。

## Route Chaining / 自动质量门

Forge 不应该依赖用户知道完整工程流程。实现、配置、脚本或运行文档被修改后，Forge 会自动把用户带到下一步质量门，例如 diff review、验收、交接检查或下一批任务确认。

例如，Engineering Delivery 做完后，不应该只说“完成”，还应该提示：

```text
Next gate: 需要先做一次 Review/Submit 自查，再判断能不能提交。
```

如果用户明确说“不要 review / 直接结束”，Forge 可以停止，但应简短提醒被跳过的风险。

## Next Step Protocol / 下一步协议

Forge 不应该让用户猜流程。每完成一个有意义的步骤，Forge 都应该给出明确的下一步。小任务只给一句；不确定时给 2-3 个选项；工程实现完成后自动指向 review、验收、文档、交接或下一批任务。

例如：

```text
下一步：进入 Review/Submit 自查，先检查 diff、测试、文档和风险，再判断能不能提交。
```

如果选项都不满意，用户可以直接补充限制条件，Forge 应重新收束方案，而不是强推原方案。

```text
Forge: 做完每一步后，直接告诉我下一步该干什么。
```

```text
Forge: 给我 3 个下一步选项；如果都不合适，再问我限制条件。
```

## Capability Hints / 能力提示

Forge 不应该假设用户知道所有隐藏能力。对于非小任务，如果有一个可选能力能明显帮用户降低风险、节省时间或发现更好的路径，Forge 会给一条很短的“可选增强”。

它不是强制下一步，也不是功能广告。用户不理会就继续主流程；小任务默认不提示；Token Saver 下最多提示一个。

例如：

```text
下一步：先按 v0.1 范围做最小可运行原型。
可选增强：如果你不确定这个方向是否已有成熟方案，可以先让我做一次开源/竞品参考。
```

```text
下一步：进入 Review/Submit 自查。
可选增强：如果这是长期项目，我也可以帮你更新 PROJECT_STATE，方便后面接着做。
```

你也可以直接说：

```text
Forge: 做的时候顺便提示我有哪些可选增强能力，但不要一次列太多。
```

```text
Forge: 不要推荐可选能力，只给主流程。
```

## Work Summary / 工作总结

Forge 不会每次都生成长报告。小任务默认不报告，或者只用一句话收尾；非小任务会在结尾给简短工作总结；阶段性交付、handoff、准备给负责人看，或用户明确要求时，才生成正式项目进展报告。

```text
Forge: 干完这轮后，给我一个简短工作总结。
```

```text
Forge: 用项目经理的方式总结这次进展。
```

```text
Forge: 给我一份可以发给负责人看的阶段报告。
```

如果你不想要总结，可以直接说：

```text
Forge: 这轮不要写报告，直接给结果。
```

## Lite Mode

Forge 有完整方法论，但小任务不会强行跑全流程。

适合 Lite Mode 的情况：

- 只写一段 README
- 只生成一个 commit message
- 只解释一个报错
- 只检查一小段 diff
- 只给一个运行命令

Lite Mode 会直接回答，并只附带必要的验证步骤。只有任务模糊、风险高、涉及架构/部署/安全/长期维护时，才会升级到完整 Forge 流程。

## Forge 的方法论

Forge 不只是写代码，而是按一套可重复执行的项目推进流程工作：

1. **Clarify：问清楚**
   先确认目标用户、使用场景、输入、输出、平台和交付形式。

2. **Scout：找参考**
   需要时先查开源项目、同类产品、官方文档和成熟做法，不凭空设计。

3. **Scope：砍 MVP**
   明确第一版必须做、可以顺手做、明确不做、后续再做。对于有价值但时机不对的想法，放入 Idea Backlog，而不是直接丢掉。

4. **Build：做原型**
   优先跑通最小闭环，让项目能运行、能看到效果、能演示。

5. **Orchestrate：调度 AI 干活**
   把目标拆成任务单，判断哪些交给人、哪些交给 AI，生成低消耗提示词，定义验收标准，必要时生成返工提示词。

6. **Automate：自动推进**
   把目标拆成选项、任务队列和小批次动作，让用户选择路线；遇到删除、部署、发布、付费、提交等风险动作时暂停确认。

7. **Stabilize：稳定迭代**
   小步修 bug、补配置、补异常、补日志、补测试、补文档。

8. **Review：检查质量**
   检查 diff、依赖、配置、兼容、安全、测试和提交风险。

9. **Document：写给别人**
   README、Quick Start、API、部署、故障排查都要面向真实用户，而不是只写给本机。

10. **Ship：交付**
   准备提交说明、MR/PR 描述、演示路径、已知限制和交接文档。

11. **Reflect：复盘沉淀**
   记录做得好的地方、踩坑、可复用经验、下一轮计划。

### AI 项目经理模板

当你想让 Forge 支配 AI 干活时，优先使用这些模板：

- `AI_TASK_BRIEF.md`：把目标拆成一个清楚的 AI 任务包。
- `AGENT_WORK_ORDER.md`：给当前 agent 角色视角使用的有边界执行提示词。
- `ROLE_WORK_ORDER.md`：当前 agent 角色任务单；需要外部工具时由用户手动复制。
- `MULTI_AGENT_PLAN.md`：多智能体协作时，人类看的角色和任务索引。
- `AGENT_INDEX.json`：多智能体协作时，AI 之间看的机器索引。
- `AGENT_INDEX.schema.json`：多智能体 JSON 索引的结构说明。
- `AGENT_TASK_CARD.md`：单个 agent 的边界清楚任务卡。
- `ACCEPTANCE_CHECK.md`：AI 做完后用于验收结果。
- `REWORK_PROMPT.md`：验收不通过时生成返工提示词。
- `EXECUTION_LOG.md`：记录任务、执行者、证据、验收结论和下一步。
- `FIELD_TEST_REPORT.md`：用真实项目试跑 Forge 后，记录证据、摩擦点、风险和下一步改进。
- `FORGE_INDEX.md`：人类可读的统一项目/路线/产物/风险/证据/下一步索引。
- `forge_index.json`：机器可读的统一事实索引，供 AI、脚本、多智能体和后续路由使用。
- `FORGE_DOCTOR_REPORT.md` / `forge_doctor.json`：Forge Doctor 稳定性总检输出。
- `PLUGINIZATION_PLAN.md`：规划未来 router skill、子 skill、共享模板/脚本和迁移门禁。
- `ROUTER_CONTRACT.json`：机器可读的自然触发、路线、reference、输出、证据和交接契约。
- `ROUTER_PROMPT_CORPUS.json`：自然触发、token 模式和双索引预期的回归样例。
- `ROUTER_TEST_REPORT.md`：记录路由模拟、预期/实际路线、发现问题和修复建议。
- `RELEASE_CHECKLIST.md`：发布前检查验证命令、Skill 校验、测试、git、tag、风险和下一步。

Forge 的项目经理原则是：先定义任务和验收标准，再交给 AI 执行；AI 做完后先验收，不合格就小范围返工，不让执行者无限制重写项目。

### 项目管理与自动化模板

`assets/templates/` 中包含这些长期项目模板：

- `PROJECT_STATE.md`：记录项目目标、当前阶段、已完成、风险、下一步。
- `DECISION_LOG.md`：记录关键技术/产品决策，方便以后解释为什么这么做。
- `IDEA_BACKLOG.md`：记录有价值但当前版本不做的想法，并写清楚什么时候重新评估。
- `RETROSPECTIVE.md`：每轮迭代后复盘.
- `PROJECT_HANDOFF.md`：把项目交给朋友、同事、老师、reviewer 或未来的自己。
- `WORKSPACE_SUMMARY.md`：接手已有工程前，记录项目识别、已有资料、验证线索、风险和下一步。
- `WORK_SUMMARY.md`：轻量记录本轮完成、产出、验证、风险和下一步。
- `BOSS_REPORT.md`：阶段性项目进展报告模板，适合 milestone、release、handoff 或给负责人看。
- `FIELD_TEST_REPORT.md`：实战闭环报告模板，适合验证 Forge 自查、多智能体规划和交付路线。
- `PLUGINIZATION_PLAN.md`：插件化路线模板，适合未来从单 skill 拆成 router + 子能力。
- `RELEASE_CHECKLIST.md`：发布检查模板，适合打 tag 或对外发布前使用。

自动化相关模板：

- `AUTOMATION_PLAN.md`：记录目标、选项、自动化等级、完成标准和暂停条件。
- `OPTION_SET.md`：记录多个可选方案，方便用户选择或补充约束。
- `TASK_QUEUE.md`：把目标拆成可推进的任务队列，支持 Human、当前 agent 角色、Manual Review、人工外部交接等执行路径。

初始化项目状态文件：

```bash
python scripts/state_initializer.py /path/to/project
```

初始化自动化推进文件：

```bash
python scripts/automation_initializer.py /path/to/project
```

如果文件已存在，默认不会覆盖；需要覆盖时加 `--force`：

```bash
python scripts/state_initializer.py /path/to/project --force
python scripts/automation_initializer.py /path/to/project --force
```

这些脚本只是生成模板和计划文件，不会替用户删除、部署、发布、提交、调用其他模型或跨工具调度。

## 安装 / 放置方式

### GitHub 源码安装

如果你从 GitHub 使用 Forge，建议按 tag 取稳定版本：

```bash
git clone https://github.com/JYSimilar/Forge.git
cd Forge
git checkout <latest-tag>
```

例如当前稳定版：

```bash
git checkout v2.2
```

如果你要继续参与迭代，可以留在 `main`；如果只是使用，优先选 GitHub Releases 里的最新 tag。

### Claude 网页版 / 桌面版

直接上传 `forge.zip` 即可。一般不用解压，也不用改成 `.skill` 后缀。

### Claude Code 全局使用

```bash
unzip forge.zip
mkdir -p ~/.claude/skills
mv forge ~/.claude/skills/
```

最终结构应为：

```text
~/.claude/skills/forge/SKILL.md
```

### Claude Code 项目内使用

在项目根目录执行：

```bash
mkdir -p .claude/skills
unzip forge.zip
mv forge .claude/skills/
```

最终结构应为：

```text
你的项目/.claude/skills/forge/SKILL.md
```

### Codex / OpenAI Agent 使用

如果你的环境支持 Codex skills，可以放到个人 skills 目录：

```bash
unzip forge.zip
mkdir -p ~/.codex/skills
mv forge ~/.codex/skills/
```

最终结构建议为：

```text
~/.codex/skills/forge/SKILL.md
```

如果你的 Codex 环境使用项目内 skills，也可以放到项目的 `.codex/skills/forge/`。不同客户端的目录可能略有差异；关键是让 `forge/SKILL.md` 位于可被 skills 系统发现的目录下。

### 发布前检查

正式打 tag 或对外发版本前，建议使用 `RELEASE_CHECKLIST.md`，至少确认：

- `quick_validate.py .` 通过；
- 测试和脚本语法检查通过；
- git 状态干净；
- zip、缓存、日志和本地运行产物没有进仓库；
- tag 指向正确 commit。

## Examples

`examples/` 目录提供了几条完整使用示例：

- `ai_note_tool_workflow.md`：从想法到 AI 小工具 MVP。
- `diff_review_workflow.md`：提交前 diff 自查。
- `non_technical_user_workflow.md`：普通人从 0 搭项目。
- `existing_project_audit_workflow.md`：接手已有工程前的工作区自查。
- `multi_agent_collaboration_workflow.md`：多智能体分工、索引、校验和状态更新。
- `automation_goal_workflow.md`：目标自动化推进。
- `ai_orchestration_workflow.md`：Forge 如何拆任务、派给 AI、验收和返工。

## 目录说明

- `SKILL.md`: skill 入口、触发路由和核心规则。
- `references/`: 按需读取的详细工作流，包括头脑风暴、工程交付、AI 调度、diff review、文档兼容、开源与竞品侦察。
- `scripts/`: 自查、diff review、文档索引、脚手架、想法评分脚本。
- `assets/templates/`: 可复制到项目里的文档模板。
- `examples/`: 面向普通用户、diff review、自动化目标推进等完整示例。
- `agents/openai.yaml`: 可选的 Codex / OpenAI Agent UI 元数据；Claude 或 Claude Code 使用时可以忽略，不影响 Forge 主功能。

## 可选文件说明

`agents/openai.yaml` 只是给部分兼容 OpenAI / Codex Agent 的工具读取的元数据。
如果你使用 Claude 网页版、Claude 桌面版或 Claude Code，不需要配置它，也不需要删除它。

## 常用脚本

```bash
python scripts/project_audit.py /path/to/project
python scripts/diff_review_helper.py /path/to/project
python scripts/new_project_scaffold.py /path/to/project
python scripts/doc_index_builder.py /path/to/project > DOC_INDEX.md
python scripts/idea_ranker.py ideas.csv
python scripts/reference_ranker.py references.csv
python scripts/state_initializer.py /path/to/project
python scripts/automation_initializer.py /path/to/project
python scripts/field_test_runner.py /path/to/workspace --out-dir /path/to/out
python scripts/router_contract_validator.py assets/templates/ROUTER_CONTRACT.json --simulate "这个仓库有什么问题？"
python scripts/dual_index_builder.py /path/to/workspace --out-dir /path/to/out
```

版本更新可查看 `CHANGELOG.md`。

## 使用建议

如果你还只有一个想法，先让 Forge 发散和收束。
如果你不确定别人有没有做过，先让 Forge 查找开源参考和同类产品设计，再决定第一版怎么做。
如果你已经有代码，先让 Forge 看项目健康度或 diff。
如果你准备给别人用，优先补 Quick Start、配置说明、测试说明和故障排查。
如果你只是自然地问“下一步怎么办”“能不能提交”“怎么写成当前 agent 可执行任务单”，Forge 应该自动启用对应流程，不需要你背命令。
