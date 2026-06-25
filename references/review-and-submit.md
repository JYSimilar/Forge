# Review And Submit

Use this for code review, diff self-checks, commit messages, PR/MR descriptions, and submit readiness.

## Code Review Mode

Lead with findings, ordered by severity. Include file and line references when available.

For each finding:

- State the bug or risk.
- Explain the impact.
- Point to the relevant file/line.
- Suggest the smallest useful fix.

Then include open questions, test gaps, residual risk, and a short summary. If there are no findings, say so clearly and mention remaining verification gaps.

## Diff Self-Check

Run `scripts/diff_review_helper.py <project>` when possible. Then inspect the actual diff for:

1. Scope: unrelated files, large formatting churn, cache, logs, virtualenvs, build outputs, secrets.
2. Intent: why each changed file changed and whether the behavior matches the request.
3. Risk: old behavior, config loading, API compatibility, data formats, permissions, cache logic, errors, deployment.
4. Tests: normal, error, boundary, regression, and whether assertions verify outcomes.
5. Docs: README, config, API docs, example commands, known issues.
6. Commit message clarity.

## Submit Readiness Output

Use this shape:

1. Change summary
2. Main files changed
3. Purpose of each file change
4. Findings or risks
5. Test coverage and commands run
6. Manual verification steps
7. Submit conclusion: `可以提交`, `建议修改后提交`, or `不建议提交`
8. Recommended commit message
9. Short note for reviewer

## Commit Messages

Prefer clear conventional style when useful:

- `feat: add <capability>`
- `fix: handle <failure mode>`
- `docs: update <doc topic>`
- `test: cover <behavior>`
- `refactor: simplify <area>`

Keep the message honest and scoped to the actual diff.

## PR/MR Descriptions

Use `assets/templates/mr_description.md` as a starting point when the user asks for a full description. Include:

- What changed
- Why it changed
- How it was tested
- Risk and rollback notes
- Follow-up items

## Reviewer Questions

Prepare answers for:

- Why this scope?
- What alternatives were considered?
- How is compatibility preserved?
- What happens on failure?
- How was this tested?
- What is intentionally deferred?

## Auto Entry After Engineering

Review/Submit should be offered or run automatically after Engineering Delivery creates or changes files. Treat this as a project quality gate, not as an optional user-discovered command.

When entering from Engineering Delivery, start with:

1. changed files / scope,
2. findings by severity,
3. tests or verification,
4. submit conclusion.

If the diff is unavailable, ask the user to provide the diff or run `scripts/diff_review_helper.py <project>` and paste the output.
