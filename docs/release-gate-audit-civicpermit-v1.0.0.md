# CivicPermit v1.0.0 Release-Gate Audit

Date: 2026-05-21

## 1. Executive Audit

- Scope: `C:\Users\scott\OneDrive\Desktop\Claude\civicpermit`
- Mode: release-gate
- Local vs live: local branch `release/civicpermit-v1-public-use`, started from `origin/main` `9b3db542a45f1c357e8ff820c6a9c99920fd5b3f`
- Pre-edit parity: local release branch was created from live `origin/main`
- Static audit confidence: High
- Runtime sign-off confidence: High for local Windows/browser/release-gate evidence; CI remains pending until push.
- Release verdict: No unresolved Blocker or Critical findings after the install/bootstrap fix.

## 2. Audit Coverage Ledger

| Lane | Status | Evidence |
|---|---|---|
| Remote parity | Checked | `git fetch origin`; release branch created from `origin/main` `9b3db542a45f...` |
| Local-vs-live commit truth | Checked | Dirty worktree contains the v1.0.0 release diff |
| CI/workflow presence | Checked | `.github/workflows/verify.yml` runs `scripts/verify-release.sh` |
| Windows install path | Checked | Native PowerShell tests, docs gate, Ruff, and release script run on this machine |
| Linux/WSL install path | Planned in CI | GitHub Actions verify and release workflows run on Ubuntu after push/tag |
| Platform parity verdict | Partially checked | Windows local path verified; Linux CI pending until push; macOS not claimed |
| First boot | Checked | `uvicorn civicpermit.main:app --host 127.0.0.1 --port 18154`; `/health` ok |
| Required post-install steps | Checked | Fresh wheel install now resolves CivicCore release wheel |
| Migrations | Not applicable | No Alembic migration system; SQLAlchemy creates local schema/tables |
| Seed/bootstrap requirements | Checked | default permit requirements seed on repository initialization |
| Runtime dependency truth | Checked | CivicCore v1.1.0 direct wheel reference verified |
| Secrets/credential handling | Checked | staff routes require local API key and trusted headers; no hardcoded secret found |
| Auth/session handling | Checked | no browser sessions; staff API-key/header gate is documented as local safeguard |
| Authorization/role boundaries | Checked | staff queue/intake routes reject missing/spoofed staff key |
| Sensitive-data exposure | Checked | persisted staff queue routes are staff-only |
| Audit/compliance logging | Partially checked | records-ready export and queue provenance exist; no hash-chain audit log claimed |
| External/admin surfaces | Checked | no live external calls; local adversarial mock endpoint only |
| Connector completeness | Checked | no connector writeback claimed |
| Connector docs truth | Checked | docs state no live GIS/LLM/permitting-system writeback |
| Background jobs/schedulers | Not applicable | none claimed |
| Frontend critical journey | Checked | `/civicpermit` desktop/mobile Playwright pass |
| Loading/empty/error/partial states | Checked | static UI state documented; API error path verified |
| Accessibility cues | Checked | skip-link focus verified |
| Docs truthfulness | Checked | README/manual/security/docs index updated to v1.0.0 |
| Version consistency | Checked | `scripts/verify-release.sh` passed |
| Release artifact consistency | Checked | wheel, sdist, `SHA256SUMS.txt` generated for v1.0.0 |
| Test realism | Checked | 31 tests include persistence, auth, queue lifecycle, adversarial mocks |
| Runtime/build/test verification | Checked | Windows tests, Ruff, docs gate, build gate, and release verifier passed |
| Browser verification | Checked | screenshots and raw evidence JSON saved |
| Prior audit challenge | Checked | install/bootstrap defect found and fixed |

## 3. Claim Verification Matrix

| Claim | Source | Verdict | Evidence |
|---|---|---|---|
| CivicPermit is v1.0.0 | README, package metadata | True | `pyproject.toml`, `__version__`, release gate |
| Depends on CivicCore v1.1.0 | README, health | True | fresh wheel install and `/health` returned CivicCore `1.1.0` |
| Staff review queues are shipped | README/manual/API | True | tests cover create/list/patch/summary and auto-queue on deficient intake |
| No permit approvals or official completeness decisions | README/UI/API boundary | True | UI warning, root message, mock rejection tests |
| Adversarial mocks replace external deployment proofs | docs/tests | True | `tests/test_integration_adversarial_mocks.py` |
| Public UI is browser-tested | QA docs | True | Playwright desktop/mobile screenshots and zero console messages |
| Release gate passes | scripts | True | Windows `scripts/verify-release.sh` passed |

## 4. What The Dev Team Needs To Do Now

No Blocker/Critical remains in local evidence. Before release publication, push the branch, open/merge the PR, tag `v1.0.0`, publish artifacts, and confirm GitHub Actions green.

## 5. Next-Sprint Watchlist

- Replace local API-key staff gate with suite identity/tenant controls when CivicCore shared auth is adopted by this module.
- Keep official municipal deployment proof out of the v1.0.0 gate; current release proof uses local adversarial mocks and CI.
- Consider Alembic migrations if CivicPermit grows beyond create-on-start local schemas.

## 6. Engineering Deep Dive

Checked `main.py`, `persistence.py`, `integration_mocks.py`, and tests. Staff queue state is persisted through SQLAlchemy when `CIVICPERMIT_INTAKE_DB_URL` is set. Public deterministic mode remains available when persistence is unset.

Finding fixed during audit:

- `BOOT-001`
  - Severity: Critical
  - Confidence: High
  - Evidence type: Runtime
  - Status: Fixed
  - Why it matters: the built wheel previously referenced an unpublished CivicCore dependency, which made fresh installs fail.
  - Evidence: fresh wheel install failed before the dependency was moved to the published CivicCore release wheel.
  - Fix: changed dependency to the published CivicCore v1.1.0 wheel URL and enabled Hatch direct references.
  - Retest: fresh Windows release gate installed `dist/civicpermit-1.0.0-py3-none-any.whl`; `/health` returned CivicPermit `1.0.0` and CivicCore `1.1.0`.

## 7. Security And Authorization Deep Dive

Checked staff headers, configured staff key behavior, spoofed key tests, and docs. Staff queue and persisted intake surfaces require `CIVICPERMIT_STAFF_API_KEY`, `X-CivicPermit-Role: staff`, and matching `X-CivicPermit-Staff-Key`. No hardcoded credential was found.

## 8. UI/UX Deep Dive

Checked `/civicpermit` with Playwright at 1440 x 1000 and 390 x 844. Console messages were empty. Skip-link focus works. Boundary warning is visible and direct.

Evidence:

- `docs/qa/current-civicpermit-release-qa/resident-desktop.png`
- `docs/qa/current-civicpermit-release-qa/resident-mobile.png`
- `docs/qa/current-civicpermit-release-qa/docs-desktop.png`
- `docs/qa/current-civicpermit-release-qa/health-json.png`
- `docs/qa/current-civicpermit-release-qa/summary.json`

## 9. Product/PM Deep Dive

The v1.0.0 scope matches the CivicSuiteUnifiedSpec role for a permit pre-application and intake-readiness product. The release does not claim permit approval, official completeness, fee calculation, inspection scheduling, live GIS/LLM, writeback, or system-of-record behavior.

## 10. Documentation Deep Dive

Checked README, text README, user manual, text manual, security notes, changelog, implementation plan, reconciliation, docs index, browser QA, and careful-coding evidence. Current-facing docs reflect v1.0.0.

## 11. Install / Bootstrap / Seeding Deep Dive

Native Windows release gate and fresh wheel install were run. Default requirement seed data is initialized by `PermitIntakeRepository`. PostgreSQL paths are supported through SQLAlchemy URL configuration; SQLite paths are covered by tests.

## 12. Version And Release Consistency Deep Dive

`scripts/verify-release.sh` checks package metadata, `__version__`, current-facing docs, tests, Ruff, build artifacts, and SHA256SUMS. It passed after the direct dependency fix.

## 13. Test Engineering Deep Dive

Collected 31 tests. Tests cover:

- runtime health/version
- requirement lookup
- validation errors
- intake readiness
- submittal outlines
- records export
- development-review context
- persisted requirement/intake records
- staff auth gates
- staff review queue lifecycle
- adversarial local mocks
- public UI copy/boundary

## 14. Runtime QA Deep Dive

Commands run:

- Windows `python -m pytest -q`: 31 passed
- Windows `bash scripts/verify-release.sh`: passed
- Windows fresh wheel install: passed through the release verifier
- Playwright desktop/mobile: passed
- Browser console: zero messages

## 15. Cross-Cutting Synthesis

CivicPermit v1.0.0 is locally release-ready after the install/bootstrap fix. The strongest residual risk is that GitHub CI and release publication have not run yet on the final pushed branch.

## 16. Verification Gaps And Sign-Off Limits

- GitHub Actions final branch/PR/tag runs are pending until push.
- Linux CI evidence is pending until push/tag.
- No external deployment proof was attempted; adversarial local mocks are the release proof for integration behavior.
