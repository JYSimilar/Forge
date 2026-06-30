# Stability Gate / Forge Doctor

Use this when Forge is preparing a stable release, checking whether its routes still work together, or the user asks for a complete project-manager self-check before handoff, release, tag, or broad iteration.

## Default Behavior

Keep this gate lightweight unless the user asks for a full report. It should collect evidence from existing Forge surfaces instead of inventing a new process:

- Workspace facts from Existing Project Audit.
- Optional `AGENT_INDEX.json` validity from Multi-Agent Collaboration.
- Optional `ROUTER_CONTRACT.json` validity and prompt corpus results from Router Contract.
- Dual Index payload consistency.
- Optional field-test JSON friction and suggested improvements.
- Release-readiness evidence when `--release` or a release/tag request is present.

## Output Contract

For non-small stability checks, produce both:

- `FORGE_DOCTOR_REPORT.md` for humans.
- `forge_doctor.json` for scripts, AI agents, or future child skills.

Each report must include:

```text
功能目标：
输入：
输出：
状态：
异常情况：
限制：
```

Then include concise sections for evidence, risks, artifacts, and 2-3 next options.

## Status Rules

- `no_project`: no clear project signal; ask the user to pick a directory, create a scaffold, or paste materials.
- `single_project`: proceed with risk, test, validation, and release evidence.
- `multiple_projects`: require target confirmation before write-heavy work or release.
- `agent_index_invalid`, `router_contract_invalid`, or `field_test_json_invalid`: return warning failure, record the errors, and do not claim stable readiness.
- `release_mode`: add release-readiness checks, but do not publish, tag, deploy, delete, or push without explicit user intent.

## Token Policy

Token Saver remains default. Use the doctor script for deterministic evidence instead of long prose. Burn Mode may include expanded matrices, but the stability conclusion and evidence standard stay the same.

## Command

```bash
python scripts/forge_doctor.py . --out-dir /path/to/out --release \
  --agent-index assets/templates/AGENT_INDEX.json \
  --router-contract assets/templates/ROUTER_CONTRACT.json
```

The target workspace is read-only. The script writes only to `--out-dir`.
