# Existing Project Audit

Use this when the user wants to inspect, continue, optimize, stabilize, or hand off an existing workspace. Forge should first find out whether there is a project before proposing implementation work.

## Triggers

- "看看这个项目", "接手这个工程", "当前工作区有什么"
- "先自查", "列一个 md 汇总", "这个项目怎么优化"
- "已有项目下一步怎么做", "放生产会不会炸"
- "帮我检测有没有项目"

Do not use this for one-line artifacts such as commit messages, small wording changes, or isolated questions.

## Workflow

1. **Detect**: check the current directory for project signals such as manifests, README, code files, tests, scripts, `.git`, and monorepo child projects.
2. **Classify**: return exactly one status: `no_project`, `single_project`, or `multiple_projects`.
3. **Summarize facts**: list project type, manifests, docs, run/test commands, languages, skipped scan notes, and obvious risks.
4. **Separate facts from assumptions**: say when something was inferred or not verified.
5. **Recommend next options**: give 2-3 concrete choices with explanations.
6. **Route onward**: after audit, continue to Engineering Delivery, AI Orchestration, Review/Submit, Docs/Compatibility, or Multi-Agent Collaboration only if useful.

## Script Support

Use `scripts/workspace_inventory.py` when a deterministic workspace summary is useful.

```bash
python scripts/workspace_inventory.py /path/to/workspace --markdown WORKSPACE_SUMMARY.md --json workspace.json --log workspace_scan.log
```

The script is read-only except for explicit output paths. It should not read or log secret values.

Use `assets/templates/WORKSPACE_SUMMARY.md` when producing a hand-edited summary.

## Output Contract

For non-trivial audits, include this layered shape:

```text
功能目标：
输入：
输出：
状态：
异常情况：
限制：
下一步：
```

Status behavior:

- `no_project`: explain that no clear project was detected and offer selecting a directory, creating a scaffold, or using pasted docs.
- `single_project`: summarize the detected project and recommend the next quality gate.
- `multiple_projects`: list root/child candidates, recommend the likely target if obvious, and ask the user to confirm before write-heavy work.

## Risk Checks

Mention concise risks when visible:

- missing README or Quick Start;
- missing tests or test command;
- no `.gitignore` in a Git project;
- unclear run command;
- caches/build artifacts/dependencies in the workspace;
- local paths, secrets, or environment-specific setup;
- multiple projects with unclear ownership;
- production concerns: deployment, rollback, logging, error handling, input validation, concurrency, and unit tests.

## Keep It Lightweight

Token Saver audit should be short: facts, risks, next options. Do not produce a long report unless the user asks for a report, milestone summary, handoff, or Burn Mode.
