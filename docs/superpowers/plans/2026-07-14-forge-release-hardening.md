# Forge 2.2 Release Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Forge v2.2 releasable and independently verifiable without expanding it into an agent runtime.

**Architecture:** Add a minimal GitHub CI and explicit MIT license at the repository boundary. Extend Forge Doctor with an opt-in, allowlisted verification runner that records redacted evidence, then improve the existing deterministic router corpus with stable metadata and aggregate metrics. Keep real-world cases as reproducible case packages; only record token and intervention measurements when they were actually observed.

**Tech Stack:** Python standard library, `unittest`, GitHub Actions, Markdown, JSON.

## Global Constraints

- `v2.2` remains the already-published stable tag; hardening work is made on a follow-up branch.
- Forge must not call other agents, access a network, install dependencies, deploy, delete files, or write in the inspected workspace.
- `--execute` accepts only inferred verification commands in a fixed allowlist and writes only under `--out-dir`.
- Command output is redacted and truncated before it is persisted.
- All claims of executed validation need command, exit code, duration, and redacted output evidence.
- Corpus cases are deterministic route-contract regression cases, not claims about model-level routing accuracy.
- Case-study metrics must state `not measured` when no real observation exists.

---

### Task 1: Release boundary and CI

**Files:**
- Create: `LICENSE`
- Create: `.github/workflows/ci.yml`
- Modify: `README.md`
- Modify: `docs/en/README.md`
- Modify: `docs/zh/README.md`
- Test: `tests/test_release_docs.py`

**Interfaces:**
- Produces a public MIT license and one CI workflow that runs on Python 3.10 through 3.13.
- Produces a README badge that links to the repository Actions page.

- [ ] **Step 1: Write failing documentation assertions**
- [ ] **Step 2: Add MIT license, CI workflow, and badge/install wording**
- [ ] **Step 3: Run documentation tests and CI-equivalent commands**
- [ ] **Step 4: Commit release boundary changes**

### Task 2: Restricted Forge Doctor execution evidence

**Files:**
- Modify: `scripts/forge_doctor.py`
- Modify: `references/stability-gate.md`
- Modify: `INDEX.md`
- Modify: `README.md`
- Test: `tests/test_forge_doctor.py`

**Interfaces:**
- Adds `--execute`, `--timeout-seconds`, and `--max-output-chars`.
- Adds `execution` to Doctor JSON with `status`, `commands`, `skipped`, and `limits`.
- Each executed command record contains `command`, `cwd`, `exit_code`, `duration_seconds`, `stdout`, `stderr`, and `status`.
- Exit code is `1` when an allowed executed command fails or times out; invalid inputs remain `2`.

- [ ] **Step 1: Write failing tests for allowlisted execution, timeout, failure, redaction, and no-command status**
- [ ] **Step 2: Add small execution helpers and wire them through payload/rendering/CLI**
- [ ] **Step 3: Run Doctor-focused tests and full unit suite**
- [ ] **Step 4: Commit Doctor execution evidence**

### Task 3: Router corpus metrics and expansion

**Files:**
- Modify: `assets/templates/ROUTER_PROMPT_CORPUS.json`
- Modify: `scripts/router_contract_validator.py`
- Modify: `assets/templates/ROUTER_TEST_REPORT.md`
- Modify: `references/router-contract.md`
- Test: `tests/test_router_contract.py`

**Interfaces:**
- Corpus scenarios add optional `language`, `intent`, and `ambiguity` metadata.
- `CorpusResult` adds `summary` with total, passed, failed, route metrics, and confusion pairs.
- Markdown reports show aggregate metrics before individual cases.
- The checked-in corpus contains at least 80 Chinese/English, conversational, ambiguous, and multi-intent regression cases.

- [ ] **Step 1: Write failing tests for aggregate metrics and metadata-compatible corpus validation**
- [ ] **Step 2: Add deterministic metrics and report rendering**
- [ ] **Step 3: Expand the corpus only with scenarios that the current contract can deterministically classify**
- [ ] **Step 4: Run corpus regression and unit suite**
- [ ] **Step 5: Commit corpus hardening**

### Task 4: Reproducible case-study package

**Files:**
- Create: `examples/cases/new-project-meeting-notes/README.md`
- Create: `examples/cases/existing-project-forge/README.md`
- Create: `examples/cases/nontechnical-personal-tracker/README.md`
- Create: `examples/cases/README.md`
- Modify: `README.md`
- Modify: `INDEX.md`
- Modify: `CHANGELOG.md`
- Test: `tests/test_release_docs.py`

**Interfaces:**
- Each case contains the original prompt, selected Forge route, generated artifacts, observed verification, risks, next choice, token measurement status, and human-intervention count status.
- Claims are limited to reproducible artifacts in the repository; unavailable measurements are recorded as `not measured`.

- [ ] **Step 1: Write failing index/content tests for three named case packages**
- [ ] **Step 2: Add concise cases that distinguish illustrative inputs from observed evidence**
- [ ] **Step 3: Link cases from product documentation without making them mandatory reading**
- [ ] **Step 4: Run documentation tests and full validation**
- [ ] **Step 5: Commit documented case studies**

### Task 5: Release verification and handoff

**Files:**
- Modify: `CHANGELOG.md`
- Test: all existing tests

- [ ] **Step 1: Run Python syntax checks, all unit tests, Skill validation, router corpus regression, and Forge Doctor with `--execute`**
- [ ] **Step 2: Inspect staged diff and ensure no generated outputs, secrets, archives, or caches are included**
- [ ] **Step 3: Commit final release notes and push the branch after explicit user approval**

## Self-Review

- Coverage: Tasks 1-4 map to the requested release/tag/CI/license, Doctor execution, route evaluation, and three case-study deliverables. Task 5 provides the requested evidence gate.
- Scope: no runtime, subagent dispatch, deployment, or cross-host functionality is introduced.
- Ambiguity resolved: execution is strictly an opt-in verifier; case-study token data is never invented.
