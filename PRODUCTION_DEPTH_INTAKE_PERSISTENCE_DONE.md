# Production-Depth Intake Persistence Done

Date: 2026-04-28

## Scope

This slice adds optional database-backed permit requirement and intake review records while preserving deterministic sample behavior when no database URL is configured.

## Shipped

- `CIVICPERMIT_INTAKE_DB_URL` enables persistent permit requirement and intake review records.
- `PermitIntakeRepository` stores seeded sample requirements and generated intake review records.
- `POST /api/v1/civicpermit/intake/review` returns an `intake_id` when persistence is configured.
- `GET /api/v1/civicpermit/intake/{intake_id}` retrieves persisted intake records when persistence is configured.

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

- Repository persistence tests must pass.
- API persistence and retrieval tests must pass.
- Full release verification must pass before push/merge.
- Browser QA evidence must confirm `docs/index.html` renders the updated persistence status at desktop and mobile widths with zero console errors.
