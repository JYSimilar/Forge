# Field Test Loop

Use this when Forge needs to validate its own project-manager workflow against a real workspace, especially after adding audit, orchestration, multi-agent, review, or delivery behavior.

## Triggers

- "用真实项目试跑 Forge"
- "验证 Forge 的自查/多智能体规划好不好用"
- "把这轮使用中的摩擦点沉淀成下一版改进"
- "先跑一遍 field test / 实战闭环"
- "看看 Forge 这套流程在这个项目上会不会卡住"

Do not use this for tiny artifacts, direct commit messages, or normal implementation work. Field testing is for validating Forge behavior, not for changing the target project.

## Workflow

1. **Pick target**: use the current workspace or a user-provided project directory.
2. **Run inventory**: use `workspace_inventory.py` or manually apply Existing Project Audit.
3. **Validate optional agent index**: if `AGENT_INDEX.json` is supplied, validate it before treating multi-agent planning as ready.
4. **Record evidence**: capture detected status, routes, commands, risks, validation results, and output artifacts.
5. **Name friction**: list unclear targets, missing run/test evidence, invalid JSON, missing docs, missing tests, or route confusion.
6. **Convert to next improvements**: recommend 2-3 concrete follow-ups for Forge or the target project.

## Script Support

Use the runner when deterministic artifacts are useful:

```bash
python scripts/field_test_runner.py /path/to/workspace --out-dir /path/to/out --max-files 2000
```

Optional multi-agent validation:

```bash
python scripts/field_test_runner.py /path/to/workspace --out-dir /path/to/out --agent-index AGENT_INDEX.json
```

The script writes `FIELD_TEST_REPORT.md` and `field_test.json`. It does not call models and does not modify the target workspace.

## Output Contract

For non-trivial field tests, include:

```text
功能目标：
输入：
输出：
状态：
异常情况：
限制：
```

Then include:

- Triggered routes;
- workspace evidence;
- optional agent index status;
- friction points;
- suggested improvements;
- 2-3 next options.

## Statuses

- `no_project`: no clear project signal; ask for a directory, scaffold, or materials.
- `single_project`: one project detected; continue to the next quality gate.
- `multiple_projects`: require target confirmation before write-heavy work.
- `agent_index_valid`: optional multi-agent index passed validation.
- `agent_index_invalid`: do not proceed with multi-agent execution until fixed.
- `input_error`: workspace input is invalid or unreadable.

## Keep It Useful

Field Test is not a long report by default. Token Saver output should name the result, evidence, friction, and next options. Use Burn Mode only when the user explicitly wants a full evaluation package.
