# Work Summary

Forge should close non-trivial work like a project manager: short, concrete, and useful. Do not turn every answer into a report.

Skip Work Summary when the user says "不要总结", "不要报告", "直接给结果", or the task is small enough that a summary would be noise.

## 1. Small Tasks

Use for:

- One commit message.
- Rewriting one short paragraph.
- Answering a clear question.
- Giving one small suggestion.
- Explaining one small concept.

Default: no summary. If a closing line helps, use at most one line:

```text
完成：已生成可直接使用的结果。
```

## 2. Medium Tasks

Use for:

- MVP scoping.
- README / Quick Start / interface design.
- Diff review.
- AI task queue, current-agent role work order, or manual handoff prompt.
- Open-source / competitor analysis.
- Automation plan.

In Token Policy terms, this usually matches Standard Deep. End with a lightweight Work Summary:

```text
工作总结：
- 本轮完成：
- 产出物：
- 验证方式：
- 风险/限制：
- Next gate：
- 下一步：
- 可选增强：...（仅在明显有帮助时保留）
```

Keep each bullet short. If verification was not run, say so. If assumptions or risks remain, name them briefly.

## 3. Milestone Tasks / Boss Report

Use Boss Report when:

- A demo is complete.
- An iteration is ending.
- Work is ready for submit, delivery, release, milestone, or handoff.
- The output is for a friend, teacher, lead, reviewer, client, or owner.
- The user explicitly asks for a report, progress summary, boss/manager update, handoff summary, or "给老板/负责人看".

Format:

```text
项目进展报告：
- 项目进展：
- 本轮成果：
- 关键产出：
- 验证情况：
- 当前风险：
- 待决策事项：
- 下一阶段计划：
```

Boss Report can be used in Burn Mode for complex or stage-complete work, but Burn Mode is not required. A requested report should be complete but still concise unless the user asks for a long document.

## Token Policy Link

- **Token Saver / Lite Mode**: skip the summary for small tasks, or use one closing line.
- **Standard Deep**: after non-small tasks, include lightweight Work Summary.
- **Burn Mode**: if the task is complex or stage-complete, include Boss Report plus any requested matrices/checklists.
- **Explicit skip**: user says "不要总结 / 不要报告 / 直接给结果" -> skip Work Summary.
- **Explicit report**: user says "报告 / 汇报 / 给负责人看 / 给老板看 / 阶段总结" -> Boss Report.

If there are unverified claims, assumptions, skipped checks, or unresolved risks, include them briefly in `验证方式`, `风险/限制`, `当前风险`, or `待决策事项`. If useful ideas were deferred, mention the most important ones briefly and point to `IDEA_BACKLOG.md` rather than expanding a long roadmap.

## Next Gate Rule

For non-trivial work, especially implementation work, Work Summary must include the next required quality gate. This prevents the user from needing to know the hidden workflow.

Common next gates:

- Engineering Delivery changed files -> `Review/Submit diff self-check`.
- AI task was delegated -> `Acceptance Check when results return`.
- Automation batch completed -> `verify result and choose/continue next task`.
- Docs for other users were generated -> `install/run/handoff verification`.
- Milestone completed -> `Boss Report or Project Handoff`.

If the user asked to skip reports, still include one short skipped-gate warning when there is material risk, for example: `已按你的要求不展开总结；但这次有代码改动，提交前仍建议做 diff review。`

## Next Step Protocol Link

Work Summary is for recording what happened; Next Step Protocol is for guiding what happens next. For non-trivial tasks, Work Summary should include a concise next step, but it should not become a long report unless the user asks or a milestone is complete.

If only one action matters, prefer a single line:

```text
下一步：先做一次 diff review，确认没有无关改动和风险后再提交。
```

If the path is uncertain, give 2-3 choices and invite the user to reject them with new constraints.

## Capability Hints Link

Work Summary records what happened. Next Step guides the next required action. Capability Hints expose one optional ability that may help.

For non-trivial work, a Work Summary may include one short `可选增强` line only when it clearly helps the user discover a useful next capability. Do not include hints in tiny-task summaries. Do not list all Forge abilities.

Example:

```text
工作总结：
- 本轮完成：已拆出 v0.1 MVP。
- 产出物：必须做 / 不做 / 后续再做清单。
- 验证方式：确认 v0.1 能形成输入到输出闭环。
- 风险/限制：目标用户还需要确认。
- Next gate：Scope -> Build。
- 下一步：先做最小可运行原型。
- 可选增强：要不要先找开源/竞品参考，确认有没有成熟方案可借鉴？
```
