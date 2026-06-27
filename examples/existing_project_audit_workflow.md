# Existing Project Audit Workflow

Use this when the user points Forge at an existing folder and asks what to do next.

## User call

```text
Forge: 接手这个工程前，先帮我自查当前工作区，并根据已有资料列一个 md 汇总。
```

## Forge behavior

1. Run or manually apply `workspace_inventory.py`.
2. Return status: `no_project`, `single_project`, or `multiple_projects`.
3. Summarize detected manifests, docs, commands, tests, risks, and skipped assumptions.
4. Give 2-3 next options, for example audit risks, split tasks, or prepare multi-agent planning.

## Useful command

```bash
python scripts/workspace_inventory.py . --markdown WORKSPACE_SUMMARY.md --json workspace.json --log workspace_scan.log
```

## Expected output shape

```text
功能目标：
输入：
输出：
状态：
异常情况：
限制：
下一步：
```
