# CivicPermit

CivicPermit is the CivicSuite module for permit pre-application and development-review intake support.

Current state: **v0.2.1 corrective demotion state - deterministic scaffold; no real AI layer, full frontend, Alembic migrations, real municipal data/search, or public-use gate. The previous v1.0.0 release was published in error and is superseded by this honest sub-1.0.0 label.**. This repo contains a FastAPI package aligned to the published CivicCore v1.1.0 release wheel, health/root endpoints, documentation gates, deterministic and database-backed permit requirement lookup, staff-gated persisted intake records, staff review queues, review-required CivicZone/CivicCode context packets, adversarial local integration mocks, intake-readiness review, submittal outline support, records-ready export checklist, and accessible public sample UI at `/civicpermit`. See [docs/release-recovery-status.md](docs/release-recovery-status.md) for the local release gate, browser QA, and CI evidence.

It does **not** ship permit approvals, official completeness determinations, fee calculations, inspections, legal advice, live GIS, live LLM calls, permit-system writeback, or system-of-record behavior.

## What CivicPermit Does

- Looks up permit requirement checklists for common applicant scenarios.
- Supports locally configured requirement records through `CIVICPERMIT_INTAKE_DB_URL`.
- Returns review-required development-review context packets that can carry CivicZone and CivicCode context IDs without calling those systems live.
- Flags missing or unclear intake materials while keeping permit-counter staff responsible for official completeness review.
- Creates staff-only review queue items for persisted deficient intakes.
- Drafts submittal outlines that require staff review.
- Builds records-ready export checklists that preserve inquiry, checklist, reviewer, queue, and generated-output provenance.
- Validates local adversarial integration mocks for missing context, spoofed approvals, fee attempts, stale sources, and role spoofing.
- Demonstrates a public pre-application intake UI at `/civicpermit`.

## Developer Quickstart

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install https://github.com/CivicSuite/civiccore/releases/download/v1.1.0/civiccore-1.1.0-py3-none-any.whl
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

For WSL verification:

```bash
python3 -m venv .venv-wsl
. .venv-wsl/bin/activate
python -m pip install https://github.com/CivicSuite/civiccore/releases/download/v1.1.0/civiccore-1.1.0-py3-none-any.whl
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## API Surface

- `GET /` returns current module status and product boundary.
- `GET /health` returns package and CivicCore version information.
- `GET /civicpermit` returns the accessible public sample UI.
- `POST /api/v1/civicpermit/requirements/lookup` returns a permit requirement checklist.
- `POST /api/v1/civicpermit/context/development-review` returns review-required permit intake context with optional CivicZone/CivicCode context IDs.
- `POST /api/v1/civicpermit/integrations/mock/development-review` validates local adversarial integration payloads.
- `POST /api/v1/civicpermit/intake/review` returns intake-readiness factors; persisted records require `X-CivicPermit-Role: staff` and `X-CivicPermit-Staff-Key` when `CIVICPERMIT_INTAKE_DB_URL` is configured.
- `GET /api/v1/civicpermit/intake/{intake_id}` retrieves persisted intake records when `CIVICPERMIT_INTAKE_DB_URL` and `CIVICPERMIT_STAFF_API_KEY` are configured and both staff headers are present.
- `POST /api/v1/civicpermit/staff/reviews` creates a staff-only review queue item.
- `GET /api/v1/civicpermit/staff/reviews` lists staff-only review queue items.
- `PATCH /api/v1/civicpermit/staff/reviews/{review_id}` updates staff-only review queue status, assignment, and resolution.
- `GET /api/v1/civicpermit/staff/reviews/summary` returns staff queue counts.
- `POST /api/v1/civicpermit/submittal/outline` returns a review-required submittal outline.
- `POST /api/v1/civicpermit/export` returns a records-ready permit-intake export checklist.

Set `CIVICPERMIT_INTAKE_DB_URL` to enable persistent permit requirement, intake review, and staff review queue records. Persisted staff routes require `CIVICPERMIT_STAFF_API_KEY`, `X-CivicPermit-Role: staff`, and matching `X-CivicPermit-Staff-Key` from a trusted staff workflow. CivicPermit uses CivicCore `staff_key_gate` for timing-safe key comparison. When unset, CivicPermit continues to use deterministic in-memory sample data for public applicant guidance.

## License

Code is Apache 2.0. Documentation is CC BY 4.0.
