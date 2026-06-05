# Audit Lite - CivicPermit Schema And Readiness Gates

**Date:** 2026-06-05
**Scope:** Reviewed CivicPermit schema migration status, `civicpermit-db-status`, `/ready` and `/api/v1/civicpermit/readiness`, runtime sample-seeding removal for configured databases, docs, and regression tests.
**Reviewer:** Codex (audit-lite)

## TL;DR

Ship this slice. Configured runtime databases no longer get sample permit requirements inserted automatically, and the readiness gate remains `not-ready` until schema is current and local permit requirements are loaded.

## Severity rollup

- Blocker: 0
- Critical: 0
- Major: 0
- Minor: 0
- Nit: 0

## Findings

None.

## What's working

- Correctness: `civicpermit/main.py` creates configured runtime repositories with `seed_defaults=False`, preventing sample rows from becoming false customer-data evidence.
- Runtime: `PermitIntakeRepository.migrate()` records `SCHEMA_VERSION` in `schema_migrations`, and `schema_status()` reports dialect, version, readiness, and missing tables.
- Operator UX: `civicpermit-db-status` initializes and reports schema state with the same SQLAlchemy URL used by `CIVICPERMIT_INTAKE_DB_URL`.
- Tests: `tests/test_production_depth_intake_persistence.py` proves ready/not-ready behavior for unconfigured, empty configured, and locally loaded requirement databases.
- Docs: README, user manual, docs landing, implementation plan, milestones, and local import guide describe schema status and readiness behavior.

## Verification

- Focused readiness tests - 5 passed.
- `python -m civicpermit.db_admin --db-url sqlite:///:memory:` - reported `CivicPermit schema ready`.
- `python -m pytest tests\test_runtime_foundation.py::test_root_endpoint_states_runtime_boundary -q` - 1 passed.
- `python -m pytest -q` - 39 passed.
- `bash scripts/verify-release.sh` - PASSED; 39 passed, 1 pytest-asyncio deprecation warning, ruff passed, artifacts built.

## Escalation recommendation

No escalation needed for this slice.
