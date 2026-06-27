# Pluginization Roadmap

Use this when the user asks whether Forge can become a plugin, split into smaller skills, or route across multiple hidden capabilities like Superpowers.

## Position

Forge 1.7 remains one skill. Do not split implementation yet. Pluginization is a future architecture path after the current routes prove stable through field tests.

## Target Shape

- **forge-router**: small entry skill that chooses routes, keeps Token Saver defaults, and avoids loading heavy references.
- **forge-audit**: existing workspace detection, field tests, project summaries, and health evidence.
- **forge-orchestration**: AI work orders, multi-agent plans, task cards, and agent indexes.
- **forge-review**: diff review, submit readiness, acceptance checks, and rework prompts.
- **forge-docs**: README, Quick Start, API docs, troubleshooting, handoff, and compatibility.
- **forge-release**: release checklist, changelog, packaging, tags, and public handoff.

## Routing Contract

The router should keep the current silent activation behavior:

- tiny tasks stay Lite;
- ambiguous project work routes to the smallest useful child skill;
- child skills receive fresh, task-local context;
- shared state lives in Markdown/JSON artifacts, not chat memory;
- completion claims require evidence or an explicit unverified note.

## Migration Gates

Do not split until these are true:

1. Field tests show stable route boundaries.
2. Each child route has a compact trigger description.
3. Shared templates and scripts have clear owners.
4. Cross-skill handoff can be represented in Markdown/JSON.
5. Release and install instructions explain both single-skill and plugin forms.

## Risks

- Splitting too early can make Forge harder to install and debug.
- Duplicate references can increase token use.
- Hidden cross-skill state can make multi-agent work unreliable.
- Users may not understand which child skill failed unless the router reports evidence.

## Recommended Next Step

Keep Forge as one skill through 1.7. Use `PLUGINIZATION_PLAN.md` only to design the future split, then revisit implementation in 1.8 or later.
