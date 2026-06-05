# UI/UX Deep Dive

## Scope

Reviewed the public `/civicpermit` page, visible copy, responsive behavior, keyboard focus, loading/success/error states, and browser evidence.

## Severity Rollup

- Blocker: 0
- Critical: 0
- Major: 0
- Minor: 0
- Nit: 0

## Findings

None.

## What's Working

- The page now exposes real controls for project type, location context, and proposal note rather than a static sample-only panel.
- The lookup action has explicit loading, success, and error status text with `aria-live`.
- The no-official-action boundary remains visible in page copy and API-rendered disclaimer output.
- Desktop 1440x1000 and mobile 390x844 Playwright checks showed no horizontal overflow, no console messages, and no request failures.
- Keyboard first focus reaches the skip link, and the primary button remains a 44px-plus target on mobile.

## Evidence

- Screenshots: `docs/qa/civicpermit-stage-2026-06-05/public-desktop.png`, `docs/qa/civicpermit-stage-2026-06-05/public-mobile.png`.
- Runtime evidence: `docs/qa/civicpermit-stage-2026-06-05/walkthrough-evidence.json`.
- Route test: `tests/test_permit_foundation.py::test_public_ui_route_is_accessible_and_honest`.

