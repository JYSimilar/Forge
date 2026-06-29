# Forge 1.8 Router Contract Report

## 功能目标

把 Forge 1.7 的“插件化路线图”推进到可验证的 1.8：仍然不拆 skill，但新增 Router Contract，让自然触发、路线边界、最小 reference 加载、完成证据和未来子 skill 交接都能被机器检查。

## 输入

- 当前 Forge 1.7 仓库。
- 用户目标：把新功能做到最终版，并使用独立智能体进行试用测试。
- 独立测试智能体返回的 JSON 反馈。

## 输出

- `references/router-contract.md`
- `references/release-readiness.md`
- `assets/templates/ROUTER_CONTRACT.json`
- `assets/templates/ROUTER_CONTRACT.md`
- `assets/templates/ROUTER_TEST_REPORT.md`
- `scripts/router_contract_validator.py`
- `tests/test_router_contract.py`
- 更新后的 `SKILL.md`、`INDEX.md`、`README.md`、`QUICK_COMMANDS.md`、`references/trigger-examples.md`、`references/pluginization-roadmap.md`、`CHANGELOG.md`、`agents/openai.yaml`

## 状态

已完成 1.8 Router Contract 功能，并根据独立智能体反馈做了二次修复。

## 异常情况

独立测试智能体 Carver 发现 5 个问题：

```json
{
  "status": "issues_found",
  "summary": "router contract validates and requested prompts route correctly, but release routing, overfit triggers, broad frontend/backend triggers, pluginization index consistency, and missing path validation needed fixes"
}
```

处理结果：

- R1：Release Readiness 首读文件不一致。已新增 `references/release-readiness.md`，并让 `SKILL.md`、`INDEX.md`、`ROUTER_CONTRACT.json` 对齐。
- R2：部分触发词过拟合测试短语。已移除过长精确短语，增加更自然的 paraphrase 回归测试。
- R3：`前端` / `后端` 单词误触发多智能体。已移除单词级触发，改为 `几个 AI`、`几个模型`、`分工协作`、`AGENT_INDEX` 等明确协作意图。
- R4：Pluginization Roadmap 索引没有体现 router contract。已更新 `INDEX.md`。
- R5：validator 不检查引用文件存在。已增加 repo-relative 路径校验，允许 `none`，会发现坏 reference。

## 限制

- `router_contract_validator.py` 是确定性 smoke test，不是语义模型路由器。
- 当前仍是单 Skill 包，不做真实插件化拆分。
- 多智能体仍只生成计划、索引、任务卡和验收边界，不直接调用多个模型。
- Prompt simulation 只能覆盖已写入契约的触发词，复杂语义仍需要 Forge 本身判断。

## 现在的能力

Forge 1.8 现在可以：

- 用 `router-contract.md` 说明什么时候进入 Router Contract 能力。
- 用 `ROUTER_CONTRACT.json` 记录路线 ID、触发词、最小 reference、默认输出、完成证据和交接路线。
- 用 `router_contract_validator.py` 校验契约结构和引用路径。
- 用 `--simulate` 模拟自然语言提示会进入哪条路线。
- 在插件化前检查 route boundary，避免拆成多个 skill 后出现重复触发、错路由、隐藏状态或 token 浪费。
- 对 Release Readiness 使用发布专用 reference，不再从泛 review 文档开始。

## 验证方式

已验证：

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/*.py
python3 scripts/router_contract_validator.py assets/templates/ROUTER_CONTRACT.json
python3 scripts/router_contract_validator.py assets/templates/ROUTER_CONTRACT.json --simulate "检查这些自然调用会不会路由到正确能力"
python3 scripts/router_contract_validator.py assets/templates/ROUTER_CONTRACT.json --simulate "修复前端页面的登录按钮"
```

独立智能体也完成了只读试用，确认 8 个主样例均能路由到预期能力。

## 下一步选项

1. **继续做 1.9：Router Field Tests**
   用 20-30 条真实用户自然语言调用跑批量模拟，找错路由、漏路由和 token 浪费点。

2. **继续做 1.9：Plugin Split Design Freeze**
   不真正拆包，但把 `forge-router`、`forge-audit`、`forge-orchestration`、`forge-review`、`forge-docs`、`forge-release` 的文件归属和迁移门禁冻结下来。

3. **继续做 1.9：Prompt Corpus**
   新增 `assets/templates/ROUTER_PROMPT_CORPUS.json` 和批量测试脚本，让自然触发测试不依赖少数手写场景。
