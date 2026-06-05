# Audit Lite - CivicCore 1.2 Alignment
**Date:** 2026-06-05
**Scope:** Reviewed CivicPermit dependency, workflow, docs, and runtime-test alignment to the published CivicCore v1.2.0 wheel.
**Reviewer:** Codex (audit-lite)

## TL;DR
Ship this slice. CivicPermit now pins the same CivicCore v1.2.0 release wheel and SHA256 used by the current city-core platform, and the current-facing docs/workflows/tests have been updated together. Focused runtime tests prove `/health` reports CivicCore `1.2.0`.

## Severity rollup
- Blocker: 0
- Critical: 0
- Major: 0
- Minor: 0
- Nit: 0

## Findings

None.

## What's working
- `pyproject.toml:16` pins the published CivicCore v1.2.0 wheel with SHA256.
- `.github/workflows/verify.yml` and `.github/workflows/release.yml` install the v1.2.0 wheel before package verification.
- `tests/test_runtime_foundation.py:18` locks the v1.2.0 direct wheel dependency and rejects stale `civiccore==1.1.0` pins.
- `tests/test_runtime_foundation.py:45` verifies `/health` reports CivicCore `1.2.0`.
- Current-facing README/manual/docs references align to the v1.2.0 platform while historical v1.0.0 audit evidence remains explicitly historical.

## Escalation recommendation

No escalation needed. This is a dependency-truth alignment slice with no API contract change.
