# Engineering Delivery

Use this for building first versions, stabilizing demos, project health checks, and engineering-quality reviews.

## Version Ladder

Use only as much of this ladder as the task needs:

- v0.1: run the main loop.
- v0.2: add basic interaction, config, or interface.
- v0.3: handle errors and boundaries.
- v0.4: add tests and manual verification.
- v0.5: add README, demo docs, and deployment notes.
- v0.6: clean temporary code and improve structure.
- v0.7: add stability, cache, logs, rate limits, and compatibility.
- v1.0: make it shippable.

For each version, state goal, included work, non-goals, verification, known issues, and next step.

## Change Scope Checklist

Before editing, identify:

- Files and modules
- Public interfaces
- Config and environment variables
- New dependencies
- Docs to update
- Backward compatibility
- Platform or device support
- Regression risk

If the scope is too broad, split the work.

## Verification Checklist

Choose checks that fit the risk:

- Normal flow
- Error flow
- Boundary values
- Repeat calls
- Config missing or invalid
- External service unavailable
- Platform or device variation
- Existing behavior regression

Report commands and outcomes. If a check was not run, say why.

## Quality Checks

- Entry points are clear.
- Responsibilities are separated.
- Names explain intent.
- Functions and files are not doing unrelated jobs.
- Config is not hard-coded.
- Errors are not swallowed.
- Logs have useful context without secrets.
- Tests assert real outcomes, not only mocks.
- Dependencies are necessary and compatible.

## Configuration

Check:

- Path handling works outside the current directory.
- Environment variables can override local config when appropriate.
- Missing or malformed config produces clear errors.
- Dev, test, and production differences are documented when relevant.
- Secrets are not committed or logged.

## Security

For user input, files, tokens, accounts, QR codes, network services, and permissions, check:

- Authentication and authorization
- Input validation
- Repeated request abuse
- Rate limiting or duplicate-submit protection
- Sensitive data in logs or responses
- Default passwords, weak tokens, or test keys in production

Use precise language such as "missing authorization check" or "DoS risk"; do not exaggerate.

## Performance And Reliability

Check:

- Repeated loading or downloading
- Cache and invalidation
- Offline or degraded mode
- Timeouts
- Infinite retry risk
- Memory, disk, or CPU pressure

Fix obvious user-impacting issues before micro-optimizing.

## Design Patterns

Use patterns only when they reduce real complexity:

- Layering: handler/controller, service, repository/DAO, config, adapter, utils, tests.
- Adapter: external APIs, models, simulators, devices, storage.
- Strategy: models, cache policies, auth rules, command parsing, export formats.
- Factory: clients and services created from config.
- Command: user instruction to system action.
- State machine: clear lifecycle states.
- Events: audit logs, notifications, status updates, error alerts.

Before using a pattern, confirm a plain function is not clearer.

## Post-Implementation Gate

Engineering Delivery does not end at "implementation done". If this route changed or generated code, config, tests, scripts, package files, execution docs, or any artifact that affects how the project runs, Forge must attach the next quality gate before closing:

1. State what changed.
2. State what verification was run or skipped.
3. State known risk.
4. Trigger Review/Submit gate: review the diff or changed files before submit.

Default closing line for Token Saver:

```text
Next gate: 需要先做一次 Review/Submit 自查，再判断能不能提交。
```

If the environment can inspect the diff safely, proceed into Review/Submit instead of waiting for the user to remember. If it cannot inspect the diff, ask a direct yes/no question: `要我现在按 Review/Submit 路线检查这次改动吗？`

Do not skip this gate just because the user did not say "review". Skip only when the user explicitly asks to stop or says they do not want review.
