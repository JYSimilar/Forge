# Idea Backlog

Use this when brainstorming, MVP scoping, version planning, retrospectives, or roadmap work produces ideas that are valuable but not right for the current version.

Forge should not throw away every idea that is cut from v0.1. Good ideas often fail only because the timing is wrong. Park them in an Idea Backlog so they can be reconsidered when the project reaches the right stage.

## When to Use

Use Idea Backlog when:

- A brainstorm produces useful ideas that are not selected now.
- MVP scoping cuts features that may matter later.
- A user says "后面再做", "先记下来", "这个以后可能有用", "以后版本再考虑".
- A feature is valuable but too large, risky, unclear, expensive, or not required for the first closed loop.
- A retrospective finds improvements worth revisiting later.
- A roadmap needs future candidates without committing to them now.

Do not use it for every rejected idea. Record only ideas with plausible future value.

## Parking Rule

When an idea is deferred, record:

- What the idea is.
- Why it is not included now.
- What condition should trigger reconsideration.
- Which version or stage might fit it.
- Priority, effort, risk, and current status.

If the user is in Token Saver mode, mention only the most important deferred ideas. In Burn Mode or roadmap work, produce a fuller backlog table.

## Status Values

Use these status values:

| Status | Meaning |
|---|---|
| Parked | Saved for later, no action now |
| Revisit | Ready to re-evaluate soon |
| Accepted | Moved into active scope or roadmap |
| Rejected | Explicitly dropped after re-evaluation |

## Priority / Effort

Use simple labels:

- Priority: High / Medium / Low
- Effort: Small / Medium / Large
- Risk: Low / Medium / High

## Output Template

```text
延后想法池：
| Idea | Why deferred | Revisit when | Target version/stage | Priority | Effort | Risk | Status |
|---|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | Parked |
```

## Revisit Triggers

Common revisit triggers:

- v0.1 main loop is stable.
- A real user asks for the feature.
- Demo succeeds and the project needs polish.
- Team/multi-user usage begins.
- More than two similar extension requests appear.
- A mock/manual step becomes the bottleneck.
- Performance, security, compatibility, or documentation becomes a blocker.
- Hardware/device/API access becomes available.
- The cost/risk of the idea drops.

## Link to MVP Scope

When scoping a first version:

- Put must-have items into MVP.
- Put tempting but unnecessary items into "第一版明确不做".
- Put valuable future ideas into Idea Backlog.
- Put harmful or misaligned ideas into "不建议做" instead of backlog.

## Link to Project State

For long-running projects, keep a short summary of the active backlog in `PROJECT_STATE.md` and keep the detailed list in `IDEA_BACKLOG.md`.

Suggested `PROJECT_STATE.md` line:

```text
延后想法：see IDEA_BACKLOG.md; next revisit after v0.1 demo is stable.
```

## Link to Retrospective

At the end of an iteration, review backlog items and mark each relevant item as:

- keep parked
- revisit next
- accept into next version
- reject

Do not let backlog become a dumping ground. If an idea has no realistic revisit condition, reject it instead of parking it.

## Examples

| Idea | Why deferred | Revisit when | Target version/stage | Priority | Effort | Risk | Status |
|---|---|---|---|---|---|---|---|
| Login system | v0.1 only needs local demo | Real users need accounts | v0.3 / stabilization | Medium | Medium | Medium | Parked |
| Plugin system | Too much architecture too early | 3+ external integrations appear | v1.0 | Low | Large | High | Parked |
| Dashboard | CLI is enough to verify core flow | Demo succeeds and users need visibility | v0.5 | Medium | Medium | Low | Parked |
| Real hardware mode | Simulator validates value first | Device access is stable | prototype -> stabilize | High | Large | High | Revisit |
