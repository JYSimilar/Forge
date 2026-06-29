# Release Readiness

Use this when the user asks whether a version can be published, tagged, installed from GitHub, or handed to other people.

## Default Flow

1. Check the current release target: version, branch, tag, and audience.
2. Verify evidence before any "ready" claim: tests, script syntax, skill validation, field-test evidence when relevant, and git hygiene.
3. Use `assets/templates/RELEASE_CHECKLIST.md` for the user-facing checklist.
4. Chain to Review/Submit when code changed, or Docs/Compatibility when install/use instructions changed.
5. Ask for explicit confirmation before pushing tags, publishing packages, deploying, deleting files, or using paid external services.

## Output Contract

Keep Token Saver by default:

- Release status:
- Evidence:
- Blocking risks:
- Next action:

Use a fuller report only when the user asks for a release report, handoff, or Burn Mode.

## Skill Repo Notes

For a Forge skill repository, useful evidence usually includes:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/*.py
python3 /Users/jysimilar/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

If publishing a tag, confirm it points at the intended commit after the commit is created.
