# Changelog

## [1.0.0] - 2026-05-21

### Changed

- Promoted CivicPermit to an honest v1.0.0 public-use module release after the active-module recovery gate.
- Synchronized package metadata, release verifier, public UI, docs, tests, browser QA evidence, release-gate audit evidence, and GitHub release workflow around the CivicCore v1.1.0 wheel pin.
- Preserved the product boundary: CivicPermit supports permit pre-application and intake readiness, but does not approve permits, make official completeness determinations, calculate official fees, schedule inspections, call live GIS/LLM systems, write back to a permitting system, or act as a system of record.

## [0.2.0] - 2026-05-11

### Changed

- feat(deps): bump civiccore pin to v1.1.0 and use shared `staff_key_gate` for timing-safe staff review queue auth.

## [0.2.0] - 2026-05-10

- Demoted the false v1.0.0 release label after the external CivicSuite audit found this module is a recovery/foundation module, not a canonical spec-complete v1 product.
- Preserved the useful recovery work while resetting the public package version to 0.2.0.
- Kept the CivicCore v1.0.0 wheel dependency at that time and pinned it with SHA256 for release integrity.
- Supersedes the prior public v1.0.0 posture; do not treat v1.0.0 as production-ready or spec-complete.

All notable changes to CivicPermit will be documented in this file.

The format follows Keep a Changelog, and this project follows Semantic Versioning.

## [Unreleased]

## [1.0.0] - 2026-05-07

### Recovery note

- The `1.0.0` label was checked through the suite release-recovery pass with a
  fresh local release gate and live browser QA. Treat the original release date
  as historical; the recovery evidence is recorded in
  `docs/release-recovery-status.md`.

### Added

- Staff review queue workflows for persisted deficient intakes, manual staff queue creation, queue listing, status updates, and queue summary counts.
- Adversarial local integration mock endpoint for CivicZone/CivicCode context, spoofed roles, attempted permit approvals, official fee attempts, stale source context, and partial context failures.
- v1.0.0 release verification surfaces, WSL verification path, and current-facing docs for shipped staff review queues.

### Changed

- Published CivicPermit release surfaces at `1.0.0`; the later suite
  release-recovery pass records fresh verification evidence.
- Updated public UI copy, root health/status copy, docs, release gate, tests, and build artifact checks to the v1.0.0 contract.

## [0.1.2] - 2026-05-07

### Added

- Production-depth intake persistence slice with `CIVICPERMIT_INTAKE_DB_URL`, persisted permit requirement records, persisted intake review records, and retrieval by `intake_id`.
- Staff-role gate for persisted intake create/read routes when intake persistence is configured.
- Development-review context contract that returns review-required permit intake context with optional CivicZone and CivicCode context IDs.

### Changed

- Aligned CivicPermit's release gate, CI install path, docs, and health-contract test with the then-published CivicCore v1.0.0 wheel.
- Updated public UI copy to v0.1.2 and removed static no-op/editable controls from the sample intake view.
- Documented the CivicCore v1.0 wheel prerequisite for clean local installs.

## [0.1.1] - 2026-04-28

### Changed

- Aligned CivicPermit to `civiccore==0.3.0` while preserving the v0.1 permit intake foundation behavior.
- Updated release gates, CI wheel install, docs, tests, and browser-visible version copy for the v0.1.1 compatibility release.

## [0.1.0] - 2026-04-27

### Added

- Professional repository scaffold, documentation, issue templates, PR template, and release gates.
- FastAPI runtime foundation with root, health, and public UI endpoints.
- Deterministic permit requirement lookup helper.
- Intake-readiness review helper with permit-counter staff review boundary.
- Submittal outline helper with human-review requirement.
- Records-ready permit-intake export checklist.
- Accessible public sample UI at `/civicpermit` with browser QA coverage.
