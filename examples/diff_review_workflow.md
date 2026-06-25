# Example: Diff Review Workflow

## User Input

```text
Forge: 帮我检查这次 diff，看看能不能提交。
```

## Forge Should Do

1. Use Lite Mode if the user only wants a quick submit check.
2. Summarize changed files.
3. Check for unrelated changes, secrets, local paths, cache files, generated artifacts, and risky dependency changes.
4. Verify tests/docs/manual checks.
5. End with one of:
   - 可以提交
   - 建议修改后提交
   - 不建议提交

## Optional Script

```bash
python scripts/diff_review_helper.py /path/to/project
python scripts/project_audit.py /path/to/project
```

## Expected Output

- findings ordered by severity
- required fixes
- suggested commit message
- reviewer note
