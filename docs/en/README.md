# Forge English Documentation

Forge turns vague work into safe, agent-executable work orders, then helps verify the result, summarize progress, and choose the next step.

## How It Works

1. You describe an idea, project problem, AI task, or next-step question.
2. Forge turns it into a bounded goal, inputs, outputs, limits, and acceptance criteria.
3. The current agent executes the work order, or you manually copy a handoff note to another tool.
4. Forge verifies the result, names risks, summarizes the work, and recommends the next step.

## Current Version

Forge 2.2 is the **Safe Work Order** release.

Core principles:

- Execute in small steps by default.
- Define a context budget before loading extra material.
- Stop at a review gate instead of pushing forward indefinitely.
- Treat cross-tool work as manual handoff only. Forge does not automatically call other models or products.

## Field Feedback

Earlier versions reduced lazy stopping, but could over-consume tokens when the user only needed a small, safe next step.

Forge 2.2 turns that feedback into product behavior: low-token Safe Work Orders with Context Budget, Stop Condition, Acceptance Criteria, and Review Gate.

## Minimal Demo

User input:

```text
I want to build a small tool that turns meeting notes into summaries. How should the first version start?
```

Typical Forge output:

```text
Goal:
Turn pasted meeting text into a structured meeting summary.

First version scope:
1. Paste meeting text
2. Output summary, action items, owners, and due dates
3. Copy the result as Markdown

Not now:
- Accounts
- Collaboration
- Audio transcription
- Calendar or Slack integrations

Work order for the current agent:
- Goal: build a local single-page prototype
- Input: one meeting transcript
- Output: structured Markdown summary
- Limits: no external API, no complex backend
- Acceptance: sample text produces summary and action items
- Verification: run the project and manually check output

Next step:
1. Build the runnable prototype
2. Add README and sample input
3. Verify whether it is ready for a friend to try
```

## Common Calls

```text
Forge: Turn this idea into a safe work order for the current agent.
```

```text
Forge: What are the 3 most important next steps for this project?
```

```text
Forge: Split this into goal, input, output, limits, acceptance, and verification.
```

```text
Forge: The AI finished. Verify the result and tell me the next step.
```

```text
Forge: Audit this workspace before we change anything.
```

More English calls are in [QUICK_COMMANDS.md](QUICK_COMMANDS.md).

## Advanced Capabilities

Advanced features stay out of the way for small tasks. Use them when the project becomes complex, release-facing, collaborative, or long-running.

- Existing Project Audit: inspect a workspace before changing it.
- Dual Index: create `FORGE_INDEX.md` for people and `forge_index.json` for AI/scripts.
- Forge Doctor: run stability and release-readiness checks.
- Multi-Agent Collaboration: plan multiple role lanes inside the current agent workflow.
- Manual Handoff: prepare copyable notes for user-managed transfer to another tool.

## Install

```bash
git clone https://github.com/JYSimilar/Forge.git
cd Forge
git checkout <latest-tag>
```

Current stable example:

```bash
git checkout v2.2
```

