# Engineering Deep Dive

## Scope

Reviewed `civicpermit/main.py`, `civicpermit/persistence.py`, `civicpermit/data_import.py`, `civicpermit/db_admin.py`, package metadata, release gates, and persistence/runtime tests.

## Severity Rollup

- Blocker: 0
- Critical: 0
- Major: 0
- Minor: 0
- Nit: 0

## Findings

None.

## What's Working

- `PermitIntakeRepository.migrate()` records `SCHEMA_VERSION` and verifies expected schema tables without destructive behavior.
- `_get_intake_repository()` uses `seed_defaults=False` for configured runtime databases, avoiding sample-data false positives.
- `import_local_requirements()` validates CSV rows before writes and uses idempotent `upsert_requirement()`.
- Staff-only persisted intake and queue routes remain guarded by CivicCore `staff_key_gate`.
- No unsafe HTML sinks, skipped tests, hardcoded staff secrets, or banned workspace path residues were found in the current audit grep.

## Evidence

- `tests/test_production_depth_intake_persistence.py` covers schema status, DB status CLI, readiness not-ready/ready paths, staff gates, persistence, and configured requirement lookup.
- `tests/test_local_requirement_import.py` covers fail-before-write import validation and idempotent updates.
- `python -m pytest -q` passed with 39 tests.
- `bash scripts/verify-release.sh` passed, including ruff and build artifacts.
