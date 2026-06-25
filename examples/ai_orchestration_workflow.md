# AI Orchestration Workflow Example

## User Request

```text
Forge: 我想让 Codex 帮我给这个项目补一个配置加载修复，你先帮我拆任务和写提示词。
```

## Forge Response Pattern

### 1. Judge Route

Current route: AI Orchestration + Acceptance Check.

Use Lite Mode only if the user asks for one prompt. Use full orchestration if the task affects project structure, tests, docs, or release readiness.

### 2. Task Split

| Task | Role | Executor | Acceptance Criteria |
|---|---|---|---|
| Fix config loading path | Builder | Codex | App loads config from project path and env override works |
| Add tests | Tester | Codex | Tests cover external working directory and missing config |
| Review diff | Reviewer | Forge / Human | No unrelated files, no secrets, no local paths |
| Update docs | Documenter | ChatGPT / Human | README explains config path and env variable |

### 3. Copyable Work Order

```text
请只修复配置加载依赖当前工作目录的问题。

目标：
- 程序从项目外目录运行时也能找到默认配置。
- 支持通过环境变量覆盖配置路径。

允许修改：
- config 相关文件
- 相关测试
- README 中配置说明（如果必要）

不要修改：
- 无关业务逻辑
- public API
- 大规模项目结构
- 依赖版本，除非确实必要

完成标准：
- 新增或更新测试覆盖从项目外目录运行的场景。
- 所有现有测试通过。
- README 或配置说明不包含本机路径。

完成后输出：
1. 改了哪些文件
2. 为什么这样改
3. 运行了哪些测试，结果是什么
4. 还有哪些风险
```

### 4. Acceptance Check After AI Returns

Forge should check:

- Did the change solve the exact task?
- Did it only touch allowed files?
- Did tests actually validate behavior?
- Did docs/config examples avoid local paths?
- Is a rework prompt needed?

Decision:

- `通过验收`
- `需要小修`
- `需要返工`
- `暂停，等用户确认`

### 5. Rework Example

```text
你上一次改动解决了默认配置路径，但没有测试环境变量覆盖。

请只补一个环境变量覆盖的测试，不要重构配置模块。

完成标准：
- 测试证明 DEVICE_ROBOT_AGENT_CONFIG 指向自定义文件时会被加载。
- 原有测试仍通过。

输出改动文件和测试结果。
```
