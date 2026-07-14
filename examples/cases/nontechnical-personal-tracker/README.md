# Case: Nontechnical Project - Personal Tracker

## Original Input

```text
I want a simple personal tracker for habits, but I do not know what to build first or how to ask an AI agent safely.
```

## Forge Route

`Clarify` -> `Project/MVP` -> `Safe Work Order` -> `Review Gate`.

## Artifacts

- First-version scope: daily habit list, check-off state, and a seven-day view.
- Exclusions: accounts, social features, notifications, and cloud sync.
- Safe Work Order: inspect only the starter files, make one local screen, verify one sample habit can be added and checked off, then stop for review.

## Verification Evidence

The acceptance check is documented but no app is bundled in this repository:

- A person can add a habit.
- A person can mark today's habit complete.
- A seven-day history remains visible after refresh if local storage is in scope.

Execution evidence is `not measured`; this is a reproducible nontechnical planning case, not a claim that Forge built an app autonomously.

## Token Measurement

`not measured` - the host agent session was not recorded.

## Human Interventions

`not measured` - no real user session has been attached to this case yet.

## Risk and Next Choice

Risk: preferences such as mobile support, reminders, and privacy can multiply scope quickly.

Choose one next step:

1. Build the local MVP from the bounded work order.
2. Ask two clarification questions about devices and persistence.
3. Stop and validate whether the tracker solves a real daily problem before building.
