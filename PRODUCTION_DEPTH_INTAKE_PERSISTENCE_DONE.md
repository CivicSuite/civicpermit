# Production-Depth Intake Persistence Done

Date: 2026-05-07

## Scope

This slice adds optional database-backed permit requirement and intake review records while preserving deterministic sample behavior when no database URL is configured. The v0.1.2 hardening pass aligns the package to CivicCore v1.0.0, gates persisted intake create/read routes to trusted staff/service workflows, bounds request text, and removes static no-op/editable controls from the public UI.

## Shipped

- `CIVICPERMIT_INTAKE_DB_URL` enables persistent permit requirement and intake review records.
- `PermitIntakeRepository` stores seeded sample requirements and generated intake review records.
- `POST /api/v1/civicpermit/intake/review` returns an `intake_id` when persistence is configured.
- `GET /api/v1/civicpermit/intake/{intake_id}` retrieves persisted intake records when persistence is configured.
- Persisted intake create/read routes require `CIVICPERMIT_STAFF_API_KEY`, `X-CivicPermit-Role: staff`, and a matching `X-CivicPermit-Staff-Key` when `CIVICPERMIT_INTAKE_DB_URL` is configured.
- Public sample UI is static and honest: no enabled no-op button and no editable text area that implies live review.
- The development-review context contract rejects unsupported summary fields instead of silently ignoring them.

## Still Not Shipped

- Permit approvals.
- Official completeness determinations.
- Fee calculations.
- Inspections.
- Legal advice.
- Live GIS or live LLM calls.
- Permit application ingestion.
- Permitting-system integrations or system-of-record behavior.

## Verification

- Repository persistence tests passed.
- API persistence, staff-role/API-key gating, and retrieval tests passed.
- `bash scripts/verify-release.sh`: 21 passed, docs gate passed, placeholder import gate passed, Ruff passed, and v0.1.2 artifacts built.
- Clean Windows venv install with the documented CivicCore wheel prerequisite followed by `python -m pip install -e ".[dev]"`: imported CivicPermit `0.1.2` and CivicCore `1.0.0`.
- Browser QA evidence must confirm `docs/index.html` and `/civicpermit` render at desktop and mobile widths with zero console errors, no page errors, no horizontal overflow, and no no-op/editable public controls.
