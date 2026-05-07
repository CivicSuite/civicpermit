CivicPermit
=========

CivicPermit is the CivicSuite module for permit pre-application and development-review intake support.

Current state: v0.1.2 permit intake foundation release plus staff-gated intake persistence, development-review context contract, and CivicCore v1 alignment. This repo ships a FastAPI package aligned to civiccore==1.0.0, health/root endpoints, documentation gates, deterministic sample permit requirement lookup, optional database-backed requirement and intake records via CIVICPERMIT_INTAKE_DB_URL, review-required CivicZone/CivicCode context packet support, intake-readiness review, submittal outline support, records-ready export checklist, and accessible public sample UI at /civicpermit.

It does not ship permit approvals, official completeness determinations, fee calculations, inspections, legal advice, live GIS, live LLM calls, permit application ingestion, permitting-system integrations, or production staff-review queues.

Core API:
- GET /
- GET /health
- GET /civicpermit
- POST /api/v1/civicpermit/requirements/lookup
- POST /api/v1/civicpermit/context/development-review
- POST /api/v1/civicpermit/intake/review; persisted records require X-CivicPermit-Role: staff when CIVICPERMIT_INTAKE_DB_URL is configured
- GET /api/v1/civicpermit/intake/{intake_id} when CIVICPERMIT_INTAKE_DB_URL is configured and X-CivicPermit-Role: staff is present
- POST /api/v1/civicpermit/submittal/outline
- POST /api/v1/civicpermit/export

Quickstart: install CivicCore first with python -m pip install https://github.com/CivicSuite/civiccore/releases/download/v1.0/civiccore-1.0.0-py3-none-any.whl, then run python -m pip install -e ".[dev]".

Set CIVICPERMIT_INTAKE_DB_URL to enable persistent permit requirement and intake review records. Persisted intake create/read routes are staff-only and require X-CivicPermit-Role: staff from a trusted staff or service workflow. When unset, CivicPermit continues to use deterministic in-memory sample data.

Code license: Apache 2.0. Documentation license: CC BY 4.0.
