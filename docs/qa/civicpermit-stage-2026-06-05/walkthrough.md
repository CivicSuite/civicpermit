# CivicPermit Stage Walkthrough

## Executive Summary

The `/civicpermit` interface is wired to the requirement lookup API and works in desktop and mobile Chromium checks. The page renders a real lookup form, submits to `/api/v1/civicpermit/requirements/lookup`, displays returned checklist details, and keeps the no-official-action boundary visible. No interface wiring findings remain.

## Methodology

- Reviewed README, user manual, route definitions, public UI source, persistence code, importer code, and tests.
- Launched `civicpermit.main:app` locally on `127.0.0.1:18164`.
- Used Playwright Chromium at 1440x1000 and 390x844.
- Captured screenshots and network/console evidence.
- Exercised `/`, `/health`, `/ready`, `/api/v1/civicpermit/readiness`, valid requirement lookup, and invalid requirement lookup.

## Project Gestalt

CivicPermit is a local-first permit pre-application support module. Its public UI exposes requirement lookup; staff-only APIs handle persisted intake and review queues; local operator tools initialize schema and import local requirements; readiness gates prevent sample fallback from being treated as customer-ready local data.

## Findings By Severity

None.

## Missing Or Partial Features

No missing UI wiring was found within the current CivicPermit stage scope. The broader suite still needs installer-level clean-machine validation outside this module stage.

## Backend Or System Capabilities Not Surfaced

The public UI surfaces requirement lookup. Staff-only persistence, staff queues, CSV import, DB status, and readiness remain documented operator/staff surfaces rather than public applicant controls, which matches the module boundary.

## Confusing Or Misleading UI

None found. The UI labels the flow as pre-application guidance and states it does not submit a formal application or make an official completeness decision.

## Broken Or Suspicious Wiring Map

| UI element or workflow | Expected system connection | Actual connection | Status | Evidence |
| --- | --- | --- | --- | --- |
| Project lookup form | POST requirement lookup API | `fetch("/api/v1/civicpermit/requirements/lookup")` | Pass | ADU checklist rendered with 4 materials |
| Loading/success status | Human-readable state update | `#lookup-status` updates during and after fetch | Pass | Playwright captured success text |
| Invalid lookup API | 422 actionable validation | Empty JSON returned 422 with detail payload | Pass | `walkthrough-evidence.json` |
| Mobile layout | No horizontal overflow | `document.body.scrollWidth <= window.innerWidth` | Pass | desktop/mobile evidence |

## Test Assessment

The current tests prove the public UI is API-wired, the requirement API validates input, local import validates before writing, configured runtime DBs do not seed samples, and readiness flips only after local requirements are loaded. The stage walkthrough adds runtime browser evidence on top of the unit/API suite.

## Recommended Repair Plan

No immediate repairs required for CivicPermit stage scope.

## Confidence And Gaps

High confidence for the local CivicPermit module gate. This walkthrough does not claim suite-level bare-metal installer readiness or cross-module end-to-end packaging readiness.

## Appendix

- Screenshot: `docs/qa/civicpermit-stage-2026-06-05/public-desktop.png`
- Screenshot: `docs/qa/civicpermit-stage-2026-06-05/public-mobile.png`
- Evidence JSON: `docs/qa/civicpermit-stage-2026-06-05/walkthrough-evidence.json`
- `python -m pytest -q` - 39 passed.
- `bash scripts/verify-release.sh` - PASSED.
