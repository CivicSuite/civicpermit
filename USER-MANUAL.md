# CivicPermit User Manual

## For Residents And Municipal Decision-Makers

CivicPermit helps cities give applicants clearer pre-application guidance before a formal permit submittal. It can show requirement context, highlight missing or unclear intake materials for staff review, route deficient persisted intakes to a staff-only queue, and produce records-ready permit-intake exports.

Current state: `1.0.0` permit pre-application product release. The module includes deterministic sample checks, optional database-backed requirement and intake records, staff review queue workflows, review-required CivicZone/CivicCode context packet support, adversarial local integration mocks, `civiccore==1.0.0` alignment, staff-only persisted intake create/read routes, and a public sample UI at `/civicpermit`.

CivicPermit does not provide legal advice, permit approvals, official completeness determinations, fee calculations, inspections, live GIS, live LLM calls, permit-system writeback, or final staff approval.

## For IT And Technical Staff

CivicPermit is a FastAPI Python package pinned to the published `civiccore v1.0.0` release wheel. The current runtime exposes:

- `GET /`
- `GET /health`
- `GET /civicpermit`
- `POST /api/v1/civicpermit/requirements/lookup`
- `POST /api/v1/civicpermit/context/development-review`
- `POST /api/v1/civicpermit/integrations/mock/development-review`
- `POST /api/v1/civicpermit/intake/review`; persisted records require `X-CivicPermit-Role: staff` and `X-CivicPermit-Staff-Key` when `CIVICPERMIT_INTAKE_DB_URL` is configured
- `GET /api/v1/civicpermit/intake/{intake_id}` when `CIVICPERMIT_INTAKE_DB_URL` and `CIVICPERMIT_STAFF_API_KEY` are configured and both staff headers are present
- `POST /api/v1/civicpermit/staff/reviews`
- `GET /api/v1/civicpermit/staff/reviews`
- `PATCH /api/v1/civicpermit/staff/reviews/{review_id}`
- `GET /api/v1/civicpermit/staff/reviews/summary`
- `POST /api/v1/civicpermit/submittal/outline`
- `POST /api/v1/civicpermit/export`

Set `CIVICPERMIT_INTAKE_DB_URL` to persist permit requirement, intake review, and staff queue records. Persisted staff routes require `CIVICPERMIT_STAFF_API_KEY`, `X-CivicPermit-Role: staff`, and matching `X-CivicPermit-Staff-Key` from a trusted staff or service workflow. Leave it unset for deterministic sample behavior.

Run local verification with:

```powershell
python -m pip install https://github.com/CivicSuite/civiccore/releases/download/v1.0/civiccore-1.0.0-py3-none-any.whl
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## Architecture

```mermaid
flowchart LR
  PublicUser["Resident or permit-counter staff"] --> CivicPermit["CivicPermit v1.0.0"]
  CivicPermit --> CivicCore["CivicCore v1.0.0"]
  CivicPermit -. released-context .-> CivicZone["CivicZone v1.0.0"]
  CivicPermit -. released-context .-> CivicCode["CivicCode v1.0.0"]
```

CivicPermit depends on CivicCore. CivicCore does not depend on CivicPermit. CivicPermit v1.0.0 uses deterministic sample requirement data plus optional staff-gated persistence, review-required context packets for released CivicZone/CivicCode references, staff review queue records, and adversarial local mocks for integration-depth validation.
