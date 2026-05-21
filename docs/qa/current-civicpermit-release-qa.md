# CivicPermit Current Release QA

Date: 2026-05-21
Scope: live local CivicPermit runtime at `http://127.0.0.1:18154`

## Summary

Live browser QA passed for the CivicPermit v1.0.0 public-use module release pass.

| Scenario | Viewport | Path | Status | Overflow | Console | Page errors | Focus evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| resident-desktop | 1440x1000 | `/civicpermit` | 200 | no | 0 | 0 | Skip to main content |
| resident-mobile | 390x844 | `/civicpermit` | 200 | no | 0 | 0 | Skip to main content |
| docs-desktop | 1440x1000 | `/docs` | 200 | no | 0 | 0 | `/openapi.json` |
| health-json | 800x600 | `/health` | 200 | no | 0 | 0 | response content rendered |

## Evidence Files

- `docs/qa/current-civicpermit-release-qa/resident-desktop.png`
- `docs/qa/current-civicpermit-release-qa/resident-mobile.png`
- `docs/qa/current-civicpermit-release-qa/docs-desktop.png`
- `docs/qa/current-civicpermit-release-qa/health-json.png`
- `docs/qa/current-civicpermit-release-qa/summary.json`

## Boundaries Checked

- Resident UI shows sample requirement lookup, intake readiness, records-ready export, and no-approval boundary copy.
- The page keeps the no-permit-approval, no-official-completeness, no-fee-calculation, and no-system-of-record boundaries visible.
- No browser console messages or page errors were observed.
- No horizontal overflow was observed at desktop or mobile widths.
- Keyboard focus reached the skip link or expected rendered browser content.
