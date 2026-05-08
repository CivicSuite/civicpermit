CivicPermit
===========

CivicPermit is the CivicSuite module for permit pre-application and development-review intake support.

Current state: published v1.0.0 label under suite-wide release-recovery review. This repo contains a FastAPI package aligned to the published CivicCore v1.0.0 release wheel, health/root endpoints, documentation gates, deterministic and database-backed permit requirement lookup, staff-gated persisted intake records, staff review queues, review-required CivicZone/CivicCode context packets, adversarial local integration mocks, intake-readiness review, submittal outline support, records-ready export checklist, and accessible public sample UI at /civicpermit. Do not promote the v1 label as a fresh product-ready claim until recovery gates, post-merge CI, and broader suite retest evidence re-earn that status.

It does not ship permit approvals, official completeness determinations, fee calculations, inspections, legal advice, live GIS, live LLM calls, permit-system writeback, or system-of-record behavior.

Core API:
- GET /
- GET /health
- GET /civicpermit
- POST /api/v1/civicpermit/requirements/lookup
- POST /api/v1/civicpermit/context/development-review
- POST /api/v1/civicpermit/integrations/mock/development-review
- POST /api/v1/civicpermit/intake/review
- GET /api/v1/civicpermit/intake/{intake_id}
- POST /api/v1/civicpermit/staff/reviews
- GET /api/v1/civicpermit/staff/reviews
- PATCH /api/v1/civicpermit/staff/reviews/{review_id}
- GET /api/v1/civicpermit/staff/reviews/summary
- POST /api/v1/civicpermit/submittal/outline
- POST /api/v1/civicpermit/export

Quickstart: install CivicCore first with python -m pip install https://github.com/CivicSuite/civiccore/releases/download/v1.0/civiccore-1.0.0-py3-none-any.whl, then run python -m pip install -e ".[dev]".

Set CIVICPERMIT_INTAKE_DB_URL to enable persistent permit requirement, intake review, and staff review queue records. Persisted staff routes require CIVICPERMIT_STAFF_API_KEY, X-CivicPermit-Role: staff, and matching X-CivicPermit-Staff-Key from a trusted staff or service workflow. When unset, CivicPermit continues to use deterministic in-memory sample data for public applicant guidance.

Code license: Apache 2.0. Documentation license: CC BY 4.0.
