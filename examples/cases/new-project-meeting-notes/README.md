# Case: New Project - Meeting Notes MVP

## Original Input

```text
I want a small tool that turns pasted meeting notes into a summary. What should the first version be?
```

## Forge Route

`Project/MVP` -> `Safe Work Order` -> `Review Gate`.

## Artifacts

- MVP scope: paste text, generate a summary, action items, owners, and due dates.
- Deferred scope: accounts, collaboration, audio transcription, and integrations.
- Bounded work order: local single-page prototype; no external API or backend.
- Full walkthrough: [`examples/meeting-notes-mvp.md`](../../meeting-notes-mvp.md).

## Verification Evidence

The documented acceptance check is: a sample transcript produces a structured Markdown summary and action list.

This repository records the planning artifact only; no runnable meeting-notes app was created as part of this case.
Execution evidence is therefore `not measured`.

## Token Measurement

`not measured` - host agent, model, and context were not recorded.

## Human Interventions

`not measured` - this is a reproducible planning walkthrough, not an observed end-user run.

## Risk and Next Choice

Risk: generated summaries may be inaccurate without a realistic sample transcript.

Choose one next step:

1. Build the local prototype with one sample transcript.
2. Collect two real meeting-note examples before implementation.
3. Stop at planning if the need is still exploratory.
