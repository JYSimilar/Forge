# Capability Hints / 能力提示

Capability Hints make hidden Forge abilities discoverable without forcing them into the main workflow.

Forge should not assume the user knows project-management options such as reference scouting, Definition of Done, multi-role review, Project State, Decision Log, Retrospective, handoff, or AI orchestration.

## Core Rule

After a meaningful step, if one optional Forge capability would materially help the user, show one short Capability Hint.

A Capability Hint is a soft recommendation, not a required next step. It should not interrupt the main workflow.

Format:

```text
可选增强：你也可以让我【能力】，适合在【场景】使用。
```

Or shorter:

```text
可选增强：要不要先做一次开源/竞品参考，避免闭门造车？
```

## Limits

- Token Saver: at most one Capability Hint per non-trivial response.
- Standard Deep: at most two hints, only when both are clearly useful.
- Burn Mode: hints may be folded into the expanded plan, but do not list every Forge feature.
- Tiny tasks: skip hints unless the user is clearly stuck.
- If the user ignores a hint, continue the main workflow. Do not repeat the same hint in every reply.
- If the user says `只给结果`, `不要推荐`, `不要提示`, or `别加可选项`, skip Capability Hints.
- Do not use hints as advertising. Only recommend a capability when it would reduce risk, save work, improve quality, or help a non-technical user discover the next useful move.

## Difference from Next Step

Next Step tells the user what should happen next.

Capability Hint tells the user about an optional Forge ability that may help.

Example:

```text
下一步：先按 v0.1 范围做最小可运行原型。
可选增强：如果你不确定这个方向是否已有成熟方案，可以先让我做一次开源/竞品参考。
```

Do not replace required quality gates with hints. If review, acceptance, verification, or handoff is the next required gate, use Next Step / Route Chaining instead.

## High-Value Hint Map

| Situation | Hint |
|---|---|
| New product or unfamiliar domain | 可选增强：要不要先找开源项目和同类产品参考，避免闭门造车？ |
| MVP scope contains many cut features | 可选增强：这些想法现在不做，但可以放进 IDEA_BACKLOG，后续版本再评估。 |
| Task begins with unclear success criteria | 可选增强：要不要先定义“怎样才算完成”，避免做完后无法验收？ |
| Project feels messy or user asks “下一步” | 可选增强：要不要我判断当前阶段，再决定下一步质量门？ |
| User wants coding or implementation help | 可选增强：要不要我把这件事写成当前 agent 可执行的角色任务单？ |
| AI executor returned work | 可选增强：要不要按 Acceptance Check 验收，不合格就生成返工提示词？ |
| A plan, prototype, doc, or submit decision is important | 可选增强：要不要从产品、工程、文档、风险几个角度快速审一遍？ |
| Project is long-running or multi-session | 可选增强：要不要生成或更新 PROJECT_STATE，方便以后接着做？ |
| A technical/product decision is made | 可选增强：这个选择以后可能会被问到，要不要记录到 Decision Log？ |
| One iteration or demo is complete | 可选增强：要不要做个轻量复盘，把经验和下一轮计划沉淀下来？ |
| Milestone is ready for a lead/teacher/client | 可选增强：要不要整理成一份能发给负责人看的阶段报告？ |
| Project is meant for another person | 可选增强：要不要生成 Project Handoff，让别人能运行和接手？ |
| Goal has many steps | 可选增强：要不要把目标拆成任务队列，按小步自动推进？ |
| User may not know Forge capabilities | 可选增强：我可以提供“找参考 / 拆 MVP / 交给 AI / 验收 / 写文档”几种路线供你选。 |

## Placement

Capability Hints usually appear after the main answer and before or after the Next Step.

Recommended order for non-trivial tasks:

```text
核心结果：...
下一步：...
可选增强：...
```

If Work Summary is present, include the hint as the final one-line optional item only when it is highly relevant:

```text
工作总结：
- 本轮完成：...
- 产出物：...
- 验证方式：...
- 风险/限制：...
- Next gate：...
- 下一步：...
- 可选增强：...
```

## Avoid

- Do not list multiple Forge abilities just because they exist.
- Do not repeat a hint the user has ignored.
- Do not hide a required gate behind optional wording.
- Do not make a simple answer feel like a product tour.
- Do not ask the user to choose from many capabilities unless they explicitly ask “Forge 能做什么”.
