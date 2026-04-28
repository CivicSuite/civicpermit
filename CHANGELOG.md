# Changelog

All notable changes to CivicPermit will be documented in this file.

The format follows Keep a Changelog, and this project follows Semantic Versioning.

## [Unreleased]

### Added

- Production-depth intake persistence slice with `CIVICPERMIT_INTAKE_DB_URL`, persisted permit requirement records, persisted intake review records, and retrieval by `intake_id`.

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
