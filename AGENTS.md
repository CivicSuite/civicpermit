# CivicPermit Agent Contract

## Source Of Truth

- Upstream suite spec: `CivicSuite/civicsuite/docs/CivicSuiteUnifiedSpec.md`, especially the CivicPermit catalog entry and suite-wide non-negotiables.
- Suite ADRs: `CivicSuite/civicsuite/docs/architecture/`.
- CivicPermit supports permit pre-application and development-review intake workflows. It does not replace permit technicians, planners, building officials, inspectors, attorneys, boards, commissions, councils, or permitting systems of record.

## Non-Negotiables

- CivicPermit never issues permits, calculates official fees, decides completeness, schedules inspections, or makes zoning, land-use, environmental, legal, entitlement, or elected-body determinations.
- Every material checklist must identify the sample intake source used.
- Submittal outlines must be marked review-required.
- Public-facing warnings must be actionable and explain the fix path.
- CivicPermit depends on CivicCore; CivicCore must never depend on CivicPermit.
- CivicPermit may reference CivicCode/CivicZone concepts only through released contracts or deterministic sample data in v0.1.0.
- Code is Apache 2.0. Docs are CC BY 4.0.

## Placeholder Package Warning

Do not import from CivicCore placeholder packages until CivicCore ships real implementations for them: `audit`, `auth`, `catalog`, `connectors`, `exemptions`, `ingest`, `notifications`, `onboarding`, `scaffold`, `search`, `verification`.

## Milestone Rule

Work one milestone at a time. When a milestone is done, report what changed, audit it once, fix findings once, re-audit once, then continue immediately unless there is a true blocker.
