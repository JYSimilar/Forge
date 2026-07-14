# Router Contract

Use this when trigger behavior is unclear, when planning a future router skill or plugin split, or when validating that Forge can choose capabilities naturally without user ceremony.

## Purpose

The router contract is Forge's handoff agreement between the current single-skill package and a future router + child-skill architecture. It defines route IDs, trigger phrases, minimum references, default outputs, completion evidence, and handoff rules in `assets/templates/ROUTER_CONTRACT.json`.

Keep routing quiet by default. Do not announce "I am entering route X" unless naming the route reduces misunderstanding.

## Default Policy

- Use Token Saver unless the user explicitly triggers Burn Mode.
- Load at most one minimum reference for the selected route by default.
- Treat "详细一点" as Standard Deep, not Burn Mode.
- Chain a second route only when it changes the next action, reduces risk, or completes a quality gate.
- For tiny tasks, choose Lite and skip route explanation.

## Routing Precedence

1. Explicit one-shot token mode request: Burn Mode changes output expansion, not the route quality bar.
2. Tiny direct artifact: Lite wins unless the user asks for review, release, or broader planning.
3. Release, submit, and safety gates: prefer Release Readiness or Review/Submit when shipping risk is explicit.
4. Existing workspace or real-project validation: prefer Existing Project Audit or Field Test Loop.
5. Multi-role AI work: prefer Multi-Agent Collaboration when the user mentions multiple models, agents, or role split.
6. Plugin/router questions: prefer Pluginization Roadmap for architecture, Router Contract for trigger and boundary validation.
7. Ambiguous ideas: Clarify or Project/MVP.

## Route Contract Fields

Each route in `ROUTER_CONTRACT.json` must include:

- `id`: stable machine-readable route name.
- `triggers`: natural phrases or keywords in Chinese or English.
- `minimum_reference`: the first reference to read, or `none`.
- `default_output`: what the user normally receives.
- `completion_evidence`: proof required before claiming done.
- `handoff`: next route or stop condition.
- `token_mode_default`: Token Saver or Standard Deep.

## Validation

Run:

```bash
python scripts/router_contract_validator.py assets/templates/ROUTER_CONTRACT.json
```

Simulate a prompt:

```bash
python scripts/router_contract_validator.py assets/templates/ROUTER_CONTRACT.json --simulate "这个仓库有什么问题？"
```

Record manual route tests with `assets/templates/ROUTER_TEST_REPORT.md` when changing triggers or route boundaries.

## Regression Corpus

`assets/templates/ROUTER_PROMPT_CORPUS.json` contains compact scenario sets for Chinese, English,
conversational, ambiguous, and multi-intent prompts. The validator expands them into individual cases
and reports total accuracy, per-route metrics, and expected-to-actual confusion pairs:

```bash
python scripts/router_contract_validator.py assets/templates/ROUTER_CONTRACT.json \
  --corpus assets/templates/ROUTER_PROMPT_CORPUS.json \
  --report /path/to/ROUTER_TEST_REPORT.md
```

This is deterministic route-contract regression evidence. It does not claim to measure a host model's
semantic routing accuracy.

## Production Boundaries

- The validator is deterministic and local; it does not call models.
- Prompt simulation is a smoke test, not a semantic router.
- Shared state belongs in Markdown/JSON artifacts, not hidden chat memory.
- Do not split Forge into multiple skills until route contracts, field tests, and release docs are stable.
