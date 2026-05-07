# CivicPermit v1.0.0 Careful-Coding Evidence

Date: 2026-05-07

## Scope

Finish CivicPermit v1.0.0 product depth without touching queued modules.

Changed areas:

- `civicpermit/persistence.py`
- `civicpermit/main.py`
- `civicpermit/integration_mocks.py`
- `civicpermit/public_ui.py`
- `tests/test_production_depth_intake_persistence.py`
- `tests/test_integration_adversarial_mocks.py`
- `tests/test_runtime_foundation.py`
- `tests/test_permit_foundation.py`
- Current-facing docs and release scripts.

## Step 1 - Callers And Consumers

- `PermitIntakeRepository` is consumed by FastAPI route helpers and persistence tests.
- `intake_review` is consumed by `POST /api/v1/civicpermit/intake/review` and API tests.
- `development_review_context` is consumed by API tests and docs.
- Version strings are consumed by `pyproject.toml`, `civicpermit/__init__.py`, root/health tests, release script, docs, and public UI tests.

## Step 2 - Runtime Context

- FastAPI route handlers are synchronous request handlers.
- SQLAlchemy calls are synchronous and local to request handling.
- Browser UI is static server-rendered HTML.
- No event-loop lock or async/sync conversion was introduced.

## Step 3 - Pattern Fan-Out

Searched for:

- `0.1.2`
- `v0.1.2`
- `production staff-review queues`
- `not shipped yet`
- `Post-v0.1.2`
- stale CivicZone/CivicCode version references

Current-facing release surfaces were updated to v1.0.0. Historical v0.1.x QA files remain historical evidence.

## Step 4 - Data Contract

New v1.0.0 contracts:

- Persisted deficient intakes return `staff_review_id`.
- Staff review queue payloads return review metadata, status, assignment, resolution, visibility, and product boundary.
- Staff summary returns total, status counts, open count, generated time, and visibility.
- Integration mock endpoint returns scenario, status, findings, review boundary, and review-required flag.

## Step 5 - Blast Radius

This changes CivicPermit's v1 API surface in `main.py`, `persistence.py`, tests, and docs. Existing v0.1.2 tests/docs assumed staff queues were unshipped; leaving those stale would create false release-readiness claims.

## Steps 6-8 - Post-Edit Path Proof

Full code path:

Staff submits persisted deficient intake -> `intake_review` validates staff headers -> `PermitIntakeRepository.create_intake_review` stores the intake -> missing fields trigger `create_staff_review_queue_item` -> response exposes `staff_review_id` -> staff lists queue -> staff patches status/resolution -> summary reflects open/resolved state.

Render/data proof:

- `staff_review_id` is asserted by `test_persisted_intake_with_missing_materials_creates_staff_review_queue`.
- Queue lifecycle is asserted by `test_staff_review_queue_lifecycle_is_staff_gated_and_persistent`.
- Integration findings are asserted by `test_integration_adversarial_mocks.py`.
- UI v1 badge and boundary warning are asserted by tests and Playwright evidence.

## Step 9 - Self-Audit

- Engineering: synchronous SQLAlchemy flow, no async deadlock or swallowed exception introduced.
- UX: public UI is static, browser-tested at desktop/mobile, zero console messages.
- QA: WSL tests and Playwright checks were run.
- Tests: new staff queue and adversarial mock behavior covered.
- Docs: README, user manual, changelog, security notes, docs index, browser QA summary, and release scripts updated.
