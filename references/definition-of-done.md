# Definition of Done

Forge should help the user know whether a task is truly done. A task is not done just because code was written or a document exists.

## Universal DoD

Every deliverable should answer:

- How to run it?
- How to verify success?
- What tests or manual checks matter?
- What docs/config changed?
- Can someone else run or understand it?
- What is intentionally unsupported?
- What known risks remain?
- What would make this not done?

## DoD by Task Type

### Idea / MVP

Done when:
- Target user and scenario are clear.
- Core pain is stated in one sentence.
- First closed loop is defined: input -> processing -> output.
- Must-do, nice-to-have, and explicit not-do items are separated.
- Success can be judged by a demo, user action, or measurable result.

Not done when the scope is still “everything” or the user path is vague.

### Prototype

Done when:
- A fresh user can follow run steps.
- The main loop produces visible output.
- Mock/demo/offline limitations are stated.
- At least one manual verification path exists.
- README or Quick Start tells where to start.

Not done when it only runs on the author's machine or needs hidden setup.

### Code Change

Done when:
- The change matches the requested scope.
- Normal and failure paths are considered.
- Tests or manual checks verify behavior, not only mocks.
- Config, docs, and dependencies are updated if behavior changed.
- Diff has no secrets, local paths, junk files, or unrelated changes.

Not done when tests pass but the real workflow was not checked and risk is unstated.

### Documentation

Done when:
- The intended audience is named: user, developer, deployer, reviewer, API caller.
- Steps are copyable and platform-specific where needed.
- Success and common failures are described.
- It avoids private paths, tokens, and author-only assumptions.

Not done when it only says “run the project” without commands or expected output.

### API / Interface

Done when:
- Caller, input, output, errors, auth, limits, and examples are defined.
- Versioning or compatibility expectations are clear if the interface may persist.
- Sensitive/internal implementation details are not exposed.
- Failure examples are included.

### Compatibility

Done when:
- Supported platforms/devices/modes are listed.
- Unsupported or unverified platforms are explicit.
- Mac/Linux, Windows PowerShell, and Docker commands are separated when relevant.
- Hardware projects have real, simulator/mock, and offline-demo thinking where possible.

### Submit / MR / PR

Done when:
- Submit verdict is clear: 可以提交 / 建议修改后提交 / 不建议提交.
- Diff summary, tests run, manual checks, risks, and reviewer notes are ready.
- Commit message or MR text reflects actual changes.

### Share / Handoff

Done when:
- Project purpose, run/test steps, directory map, config, known issues, and next steps are in a handoff doc.
- A new person knows what to try first and what not to expect.

## Compact Output Template

```text
完成标准：
1. 运行：...
2. 验证：...
3. 测试/手动检查：...
4. 文档/配置：...
5. 已知限制：...
6. 不算完成的情况：...
```
