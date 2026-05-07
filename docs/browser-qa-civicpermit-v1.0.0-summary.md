# CivicPermit v1.0.0 Browser QA

Date: 2026-05-07

## Runtime

- Server: `python -m uvicorn civicpermit.main:app --host 127.0.0.1 --port 8024`
- Browser runner: WSL Node + Playwright Chromium
- Target: `http://127.0.0.1:8024/civicpermit`

## Desktop

- Viewport: 1440 x 1000
- HTTP status: 200
- Screenshot: `docs/browser-qa-civicpermit-v1.0.0-desktop.png`
- Console messages: none
- H1: `Help applicants arrive with the right first packet.`
- Badge: `v1.0.0 permit pre-application + staff review queues`
- Boundary warning present: CivicPermit does not approve permits, calculate official fees, schedule inspections, or replace the permitting system of record.
- Keyboard/focus: first Tab focuses `Skip to main content`.

## Mobile

- Viewport: 390 x 844
- HTTP status: 200
- Screenshot: `docs/browser-qa-civicpermit-v1.0.0-mobile.png`
- Console messages: none
- Body width: 390px
- H1 and badge render without horizontal overflow.
- Keyboard/focus: first Tab focuses `Skip to main content`.

## UI States

- Success/content state: public sample checklist, intake-readiness, records-ready export, and boundary cards render.
- Empty/loading state: not applicable; `/civicpermit` is static server-rendered HTML with no client loading state.
- Error state: API validation error checked through `POST /api/v1/civicpermit/requirements/lookup` with empty JSON; response is 422 with an actionable `fix` field.
- Partial state: static public page shows non-approval warning and sample-only context rather than implying final application status.

## Evidence

- Raw evidence JSON: `docs/browser-qa-civicpermit-v1.0.0-evidence.json`
