# Dual Index

Use this when Forge needs to leave both a human-readable project index and a machine-readable AI/script index for non-trivial project work.

## When To Generate

Generate a dual index automatically for non-small work in these routes:

- Existing Project Audit;
- Field Test Loop;
- Multi-Agent Collaboration;
- Router Contract;
- Pluginization Roadmap;
- Release Readiness;
- milestone, handoff, or stakeholder-facing work.

Force it when the user asks for:

- "人类索引和机器索引"
- "双索引"
- "给人看的 md 和 AI 看的 json"
- "human index and machine index"

Skip it for tiny tasks such as commit messages, one-paragraph rewrites, small explanations, or one-off suggestions. Also skip it when the user says not to generate files or indexes.

## Contract

The human index is `FORGE_INDEX.md`. The machine index is `forge_index.json`.

Both must come from one shared payload. Do not separately infer facts for Markdown and JSON.

The JSON payload must include:

- `schema_version`
- `status`
- `workspace`
- `source_routes`
- `artifacts`
- `projects`
- `agents`
- `tasks`
- `routes`
- `evidence`
- `risks`
- `next_options`
- `limits`

## Script

Use:

```bash
python scripts/dual_index_builder.py /path/to/workspace --out-dir /path/to/out
```

Optional inputs:

```bash
--agent-index AGENT_INDEX.json
--router-contract ROUTER_CONTRACT.json
--field-test-json field_test.json
```

The script is read-only for the target workspace and writes only to `--out-dir`.

## Status And Errors

- Exit `0`: indexes were written; warnings may still appear in the payload.
- Exit `1`: optional machine input was invalid and the indexes record the risk.
- Exit `2`: workspace path or output writing failed.

Invalid optional inputs must be recorded in both Markdown and JSON. Never report success when an input index is invalid.

## Token Policy

Token Saver remains default. For normal work, generate the files and summarize only the paths, status, risks, and next option in chat. Do not paste the full indexes unless asked.
