# CivicPermit Release Recovery Status

Date: 2026-05-09
Repo: `CivicSuite/civicpermit`

## Current Verdict

`v1.0.0` exists as a published label. The suite release-recovery pass has now
rechecked the repo with the local release gate, live browser QA, documentation
truth checks, build artifacts, and current CivicCore v1.1.0 dependency
alignment. The original release date remains historical; this file records the
fresh recovery evidence.

## Recovery Gates

| Gate | Current status | Evidence |
| --- | --- | --- |
| Public claim recovery | Passing locally | README, text README, user manual, docs landing page, changelog, and docs checks now describe the v1.0.0 corrective demotion state without overstating permit approvals, official completeness determinations, fee calculations, inspections, legal advice, live GIS, live LLM calls, permit-system writeback, or system-of-record behavior. |
| Native WSL/Linux proof | Historical pass | WSL selected `.venv-wsl/bin/python3`, reported platform `linux`, and completed `VERIFY-RELEASE: PASSED`. |
| Runtime install proof | Historical pass | Fresh WSL editable install succeeded with the published CivicCore v1.1.0 release wheel and Hatch direct references enabled. |
| Security scan | Historical pass | Tracked-file secret scan returned no matches. |
| Docs-source enforcement | Passing locally | `scripts/verify-docs.sh` blocks stale product-release claims. |
| Mock-vs-production labeling | Passing locally | Existing docs distinguish local adversarial mocks, no legal advice, no permit approvals, and no live external calls by default. |
| Browser/user-flow QA | Passing locally | Playwright checked live `/civicpermit` at desktop and mobile widths plus `/docs` and `/health`; see `docs/qa/current-civicpermit-release-qa.md`. |
| Release gate | Passing locally | `scripts/verify-release.sh` passed with version checks, tests, docs gate, placeholder import gate, Ruff, package build, and SHA256 generation. |

## Current Evidence

- Local release gate on Windows: `31 passed`; docs gate, placeholder import
  gate, ruff, build artifacts, and SHA256 generation passed.
- Historical native WSL release gate: `31 passed`; docs gate, placeholder
  import gate, ruff, build artifacts, and SHA256 generation passed.
- WSL fresh install: `python -m pip install -e .[dev]` succeeded in
  `.venv-wsl`.
- Browser QA: live `/civicpermit` desktop `1440x1000` and mobile `390x844`,
  `/docs` desktop, and `/health` passed with no console messages, no page
  errors, no horizontal overflow, and keyboard focus reaching expected links or
  content.

## Sign-Off Boundary

This recovery status does not erase or rewrite the existing `1.0.0` package
version. It changes the public posture: CivicPermit's current `v1.0.0` code
path has fresh local release-gate and browser evidence. Remote PR/CI evidence is
the remaining publication step for this recovery update.
