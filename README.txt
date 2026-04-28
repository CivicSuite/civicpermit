CivicPermit
=========

CivicPermit is the CivicSuite module for permit pre-application and development-review intake support.

Current state: v0.1.1 permit intake foundation release plus production-depth intake persistence slice. This repo ships a FastAPI package aligned to civiccore==0.3.0, health/root endpoints, documentation gates, deterministic sample permit requirement lookup, optional database-backed requirement and intake records via CIVICPERMIT_INTAKE_DB_URL, intake-readiness review, submittal outline support, records-ready export checklist, and accessible public sample UI at /civicpermit.

It does not ship permit approvals, official completeness determinations, fee calculations, inspections, legal advice, live GIS, live LLM calls, permit application ingestion, permitting-system integrations, or production staff-review queues.

Core API:
- GET /
- GET /health
- GET /civicpermit
- POST /api/v1/civicpermit/requirements/lookup
- POST /api/v1/civicpermit/intake/review
- GET /api/v1/civicpermit/intake/{intake_id} when CIVICPERMIT_INTAKE_DB_URL is configured
- POST /api/v1/civicpermit/submittal/outline
- POST /api/v1/civicpermit/export

Set CIVICPERMIT_INTAKE_DB_URL to enable persistent permit requirement and intake review records. When unset, CivicPermit continues to use deterministic in-memory sample data.

Code license: Apache 2.0. Documentation license: CC BY 4.0.
