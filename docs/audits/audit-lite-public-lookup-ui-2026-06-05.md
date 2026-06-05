# Audit Lite - CivicPermit Public Lookup UI

**Date:** 2026-06-05
**Scope:** Reviewed the `/civicpermit` public lookup UI wiring, API-backed browser behavior, current-facing docs fan-out, and route tests added in the CivicPermit stage slice.
**Reviewer:** Codex (audit-lite)

## TL;DR

Ship this slice. The public page now provides a real checklist lookup form over the existing requirement lookup API, keeps the no-official-action boundary visible, and passes desktop/mobile browser checks without console errors, request failures, or horizontal overflow.

## Severity rollup

- Blocker: 0
- Critical: 0
- Major: 0
- Minor: 0
- Nit: 0

## Findings

None.

## What's working

- UX: `civicpermit/public_ui.py` exposes usable project type, location context, and proposal-note controls with explicit loading, success, and error status text.
- Correctness: the browser form posts to `/api/v1/civicpermit/requirements/lookup` and renders returned title, citation, materials, staff note, and disclaimer without changing the backend API contract.
- Tests: `tests/test_permit_foundation.py` now asserts the public page is wired to the API instead of preserving the old static sample.
- Docs: `README.md`, `USER-MANUAL.md`, `docs/index.html`, `docs/IMPLEMENTATION_PLAN.md`, and `docs/MILESTONES.md` now describe a public lookup UI rather than a static sample UI.

## Verification

- `python -m pytest tests\test_permit_foundation.py::test_public_ui_route_is_accessible_and_honest tests\test_permit_foundation.py::test_requirement_lookup_api_success_shape -q` - 2 passed.
- `python -m pytest tests\test_permit_foundation.py -q` - 11 passed.
- Playwright live check against `http://127.0.0.1:18163/civicpermit` - desktop 1440x1000 and mobile 390x844 loaded the ADU checklist, rendered 4 materials, had no console messages, had no request failures, and had no horizontal overflow.
- `python -m pytest -q` - 34 passed.
- `bash scripts/verify-release.sh` - PASSED; 34 passed, 1 pytest-asyncio deprecation warning, ruff passed, artifacts built.

## Escalation recommendation

No escalation needed for this slice.
