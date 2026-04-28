# CivicPermit

CivicPermit is the CivicSuite module for permit pre-application and development-review intake support.

Current state: **v0.1.1 permit intake foundation release**. This repo ships a FastAPI package aligned to `civiccore==0.3.0`, health/root endpoints, documentation gates, deterministic sample permit requirement lookup, intake-readiness review, submittal outline support, records-ready export checklist, and accessible public sample UI at `/civicpermit`. It does **not** ship permit approvals, official completeness determinations, fee calculations, inspections, legal advice, live GIS, live LLM calls, permit application ingestion, permitting-system integrations, or production staff-review queues.

## What CivicPermit Does

- Looks up sample permit requirement checklists for common applicant scenarios.
- Flags missing or unclear intake materials while keeping permit-counter staff responsible for official completeness review.
- Drafts a submittal outline that requires staff review.
- Builds records-ready export checklists that preserve inquiry, checklist, reviewer, and generated-output provenance.
- Demonstrates a public pre-application intake UI at `/civicpermit`.

## Developer Quickstart

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## API Foundation

- `GET /` returns current module status and next roadmap boundary.
- `GET /health` returns package and CivicCore version information.
- `GET /civicpermit` returns the accessible public sample UI.
- `POST /api/v1/civicpermit/requirements/lookup` returns a sample permit requirement checklist.
- `POST /api/v1/civicpermit/intake/review` returns sample intake-readiness factors.
- `POST /api/v1/civicpermit/submittal/outline` returns a reviewed-required submittal outline.
- `POST /api/v1/civicpermit/export` returns a records-ready permit-intake export checklist.

## License

Code is Apache 2.0. Documentation is CC BY 4.0.
