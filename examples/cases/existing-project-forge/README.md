# Case: Existing Project - Forge Release Hardening

## Original Input

```text
Prepare Forge for a trustworthy release: add CI, a license, bounded Doctor execution, route regression evidence, and release examples.
```

## Forge Route

`Existing Project Audit` -> `Stability Gate` -> `Router Contract` -> `Release Readiness`.

## Artifacts

- Workspace inventory and Forge Doctor report.
- A GitHub Actions matrix for Python 3.10 through 3.13.
- MIT License.
- Router prompt corpus and Markdown metrics report.
- This case-study package.

## Verification Evidence

Observed from this repository's release-hardening work:

- The router validator processed 115 deterministic cases and reported zero contract mismatches.
- Doctor unit tests cover allowlisting, skipped unsafe commands, failure status, and redaction.
- Final release commands are recorded in the pull-request or release handoff, not copied here as stale evidence.

## Token Measurement

`not measured` - this repository does not collect host-agent token telemetry.

## Human Interventions

Observed intervention: an implementation review corrected the CI design because the local Codex `quick_validate.py` path is unavailable on GitHub runners.

## Risk and Next Choice

Risk: the router corpus proves deterministic trigger compatibility, not live-model semantic routing quality.

Choose one next step:

1. Run the final release gate and publish a follow-up release.
2. Add observed host-agent transcripts to upgrade this into a measured field case.
3. Keep the corpus as a fast regression gate and defer broader semantic evaluation.
