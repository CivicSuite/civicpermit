# QA Deep Dive

## Scope

Reviewed the running FastAPI app, public UI, health/root/readiness endpoints, requirement lookup API, invalid request behavior, screenshots, console/request logs, and release verifier output.

## Severity Rollup

- Blocker: 0
- Critical: 0
- Major: 0
- Minor: 0
- Nit: 0

## Findings

None.

## What's Working

- `/civicpermit` loaded at desktop and mobile sizes, submitted the lookup form, rendered the ADU checklist, and produced no console messages or failed requests.
- `/`, `/health`, `/ready`, and `/api/v1/civicpermit/readiness` returned 200 during runtime QA.
- `/api/v1/civicpermit/requirements/lookup` returned 200 for valid input and 422 with actionable validation detail for empty input.
- The local server was stopped after QA, leaving no running helper process.

## Evidence

- Runtime evidence JSON: `docs/qa/civicpermit-stage-2026-06-05/walkthrough-evidence.json`.
- Screenshots: `docs/qa/civicpermit-stage-2026-06-05/public-desktop.png`, `docs/qa/civicpermit-stage-2026-06-05/public-mobile.png`.
- Release gate: `VERIFY-RELEASE: PASSED`.

