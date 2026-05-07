# CivicPermit

CivicPermit is the CivicSuite module for permit pre-application and development-review intake support.

Current state: **v0.1.2 permit intake foundation release plus staff-gated intake persistence, development-review context contract, and CivicCore v1 alignment**. This repo ships a FastAPI package aligned to `civiccore==1.0.0`, health/root endpoints, documentation gates, deterministic sample permit requirement lookup, optional database-backed requirement and intake records via `CIVICPERMIT_INTAKE_DB_URL`, review-required CivicZone/CivicCode context packet support, intake-readiness review, submittal outline support, records-ready export checklist, and accessible public sample UI at `/civicpermit`. It does **not** ship permit approvals, official completeness determinations, fee calculations, inspections, legal advice, live GIS, live LLM calls, permit application ingestion, permitting-system integrations, or production staff-review queues.

## What CivicPermit Does

- Looks up sample permit requirement checklists for common applicant scenarios.
- Returns review-required development-review context packets that can carry CivicZone and CivicCode context IDs without calling those systems live.
- Flags missing or unclear intake materials while keeping permit-counter staff responsible for official completeness review.
- Drafts a submittal outline that requires staff review.
- Builds records-ready export checklists that preserve inquiry, checklist, reviewer, and generated-output provenance.
- Demonstrates a public pre-application intake UI at `/civicpermit`.

## Developer Quickstart

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install https://github.com/CivicSuite/civiccore/releases/download/v1.0/civiccore-1.0.0-py3-none-any.whl
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## API Foundation

- `GET /` returns current module status and next roadmap boundary.
- `GET /health` returns package and CivicCore version information.
- `GET /civicpermit` returns the accessible public sample UI.
- `POST /api/v1/civicpermit/requirements/lookup` returns a sample permit requirement checklist.
- `POST /api/v1/civicpermit/context/development-review` returns review-required permit intake context with optional CivicZone/CivicCode context IDs.
- `POST /api/v1/civicpermit/intake/review` returns sample intake-readiness factors; persisted records require `X-CivicPermit-Role: staff` and `X-CivicPermit-Staff-Key` when `CIVICPERMIT_INTAKE_DB_URL` is configured.
- `GET /api/v1/civicpermit/intake/{intake_id}` retrieves persisted intake records when `CIVICPERMIT_INTAKE_DB_URL` and `CIVICPERMIT_STAFF_API_KEY` are configured and both staff headers are present.
- `POST /api/v1/civicpermit/submittal/outline` returns a reviewed-required submittal outline.
- `POST /api/v1/civicpermit/export` returns a records-ready permit-intake export checklist.

Set `CIVICPERMIT_INTAKE_DB_URL` to enable persistent permit requirement and intake review records. Persisted intake create/read routes are staff-only and require `CIVICPERMIT_STAFF_API_KEY`, `X-CivicPermit-Role: staff`, and matching `X-CivicPermit-Staff-Key` from a trusted staff or service workflow. When unset, CivicPermit continues to use deterministic in-memory sample data.

## License

Code is Apache 2.0. Documentation is CC BY 4.0.
