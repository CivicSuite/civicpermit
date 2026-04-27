CivicPermit
=========

CivicPermit is the CivicSuite module for permit pre-application and development-review intake support.

Current state: v0.1.0 permit intake foundation release. This repo ships a FastAPI package, health/root endpoints, documentation gates, deterministic sample permit requirement lookup, intake-readiness review, submittal outline support, records-ready export checklist, and accessible public sample UI at /civicpermit.

It does not ship permit approvals, official completeness determinations, fee calculations, inspections, legal advice, live GIS, live LLM calls, permit application ingestion, permitting-system integrations, or production staff-review queues.

Core API:
- GET /
- GET /health
- GET /civicpermit
- POST /api/v1/civicpermit/requirements/lookup
- POST /api/v1/civicpermit/intake/review
- POST /api/v1/civicpermit/submittal/outline
- POST /api/v1/civicpermit/export

Code license: Apache 2.0. Documentation license: CC BY 4.0.
