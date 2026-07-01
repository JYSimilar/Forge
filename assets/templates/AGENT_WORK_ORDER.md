<!-- Forge template: Agent Work Order - 给当前 agent 的某个角色视角下发有边界的执行任务时使用 -->
# Agent Work Order

Use this section as a bounded task for the current agent. If the user wants another tool to run it, the user copies it manually.

```text
You are executing one bounded task for this project.

Current Agent Context:
- Current installed agent/model:
- Role view:
- Manual handoff destination, if user-provided:

Context Budget:
- Use only the listed inputs first.
- Ask before loading broad repository context.

Acceptance First:
- Treat acceptance criteria as the contract.
- Do not claim completion without verification evidence.

Task:

Goal:

Context:

Allowed changes:

Do not change:

Do Not:
- Do not rewrite unrelated files.
- Do not add heavy dependencies without approval.
- Do not perform destructive, paid, deployment, publish, or secret-touching actions without user confirmation.
- Do not assume Forge can call another model, product, or external agent.

Implementation instructions:
1.
2.
3.

Acceptance criteria:
-

Verification required:
-

Before making broad refactors, adding heavy dependencies, deleting files, changing public interfaces, or touching secrets/configs, stop and ask.

When finished, report:
1. Files changed
2. What changed and why
3. Tests/checks run and results
4. Remaining risks
```
```
