# Context Budget Contract

Use this when the user asks to save tokens, control context, avoid loading too many files, or make Forge output host-agent work orders with a predictable context budget.

## Default

Token Saver remains the default. Start with the smallest route, one matching reference at most, and direct output.

## Route Budgets

- Lite: no reference unless needed.
- Existing Project Audit: scan facts first; read one matching reference only if the next action depends on it.
- AI Orchestration / Agent-Compatible Work: include task goal, relevant files, acceptance, and verification; avoid broad background.
- Multi-Agent Collaboration: each agent receives only its own task card and shared index pointers.
- Router Contract / Stability Gate: prefer scripts and JSON corpus over long explanation.
- Burn Mode: explicit one-shot only; can expand visible artifacts but must not change the quality bar.

## Escalation

Move from Token Saver to Standard Deep when the task is architectural, risky, ambiguous, cross-role, or release-facing. Do not enter Burn Mode unless explicitly requested with `Forge: Burn Mode`, `Forge: 燃烧模式`, or `Forge: 燃烧 token`.

## Output Rule

For host-agent work orders, include:

```text
Context Budget:
- Required context:
- Optional context:
- Do not load:
```

If context is missing, ask for the smallest missing input rather than loading unrelated materials.
