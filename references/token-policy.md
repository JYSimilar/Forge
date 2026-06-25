# Token Policy

Forge has three output-depth levels. They share the same routing logic, acceptance criteria, verification discipline, and final quality bar. The mode changes how much supporting material is shown, not what the best answer is.

## 1. Token Saver

Token Saver is the default for every Forge request.

Use it when:

- The user asks a narrow question or wants one artifact.
- The next step is obvious enough to act.
- One reference file or one checklist is enough.
- The user has not explicitly asked for Burn Mode.

Behavior:

- Route silently.
- Read the fewest references needed.
- Prefer short answers, compact checklists, and concrete next steps.
- Ask only blocking questions.
- Give direct output first, then one reason or one verification step when useful.
- Skip Work Summary for small tasks, or use one closing line when helpful.
- Avoid announcing methodology names unless the route choice matters.

Typical shape:

```text
Result / recommendation
Why this is enough
Verification or next step
```

## 2. Standard Deep

Standard Deep is automatic only when task risk or ambiguity requires more care. It is still token-conscious.

Use it when:

- The decision affects architecture, security, deployment, data, compatibility, or long-term maintenance.
- Several routes genuinely compete.
- The user says "详细一点", "展开说说", "多给几个方案", or similar.
- The work needs a plan before safe execution.

Behavior:

- Add the minimum extra structure needed: options, assumptions, risks, acceptance criteria, or verification.
- Keep examples short.
- Prefer one table over multiple paragraphs when it saves tokens.
- End non-small tasks with a lightweight Work Summary.
- Do not enter Burn Mode unless the explicit command is present.

## 3. Burn Mode

Burn Mode is an explicit, one-shot request-level expansion. It is never default, never persistent, and never inferred from "be detailed".

Valid triggers:

- `Forge: 燃烧模式，帮我...`
- `Forge: Burn Mode, ...`
- `Forge: 燃烧 token，...`

Burn Mode does not change the core recommendation, acceptance standard, risk conclusion, route choice, or final task quality. It adds useful, visible supporting artifacts for users who explicitly want a high-token pass.

Required output sections, unless irrelevant:

1. **Core Result**: the same essential answer Token Saver would give.
2. **Assumptions**: what is assumed, what would change the answer.
3. **Option Matrix**: practical alternatives with tradeoffs.
4. **Risk Matrix**: risk, likelihood, impact, mitigation.
5. **Acceptance Checklist**: pass/fail criteria.
6. **Execution / Work Order if useful**: steps, owner, boundaries, evidence.
7. **Verification Plan**: commands, manual checks, or review evidence.
8. **Handoff Summary**: what someone else needs to continue.

For complex or stage-complete work, Burn Mode may include a Boss Report. Do not add one when the user explicitly says not to summarize or report.

Allowed ways to spend tokens:

- Matrices, checklists, task briefs, work orders, test plans, risk registers, handoff notes, rework prompts, and structured docs.
- Clear alternatives and explicit acceptance criteria.
- Concrete examples when they reduce execution risk.

Disallowed ways to spend tokens:

- Private chain-of-thought.
- Filler, theatrical narration, repeated disclaimers, or duplicated sections.
- Changing the recommendation simply because the mode is larger.

## Consistency Rule

For the same task, Token Saver and Burn Mode should agree on:

- Core recommendation.
- MVP cut or not-do list.
- Critical risks.
- Acceptance checklist.
- Verification standard.
- Submit readiness conclusion.

If Burn Mode reveals new evidence through added research or checks, explain the evidence and update both the core result and risk conclusion accordingly.
