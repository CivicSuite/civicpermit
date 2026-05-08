# CivicPermit Release Recovery Status

Date: 2026-05-07
Repo: `CivicSuite/civicpermit`

## Current Verdict

`v1.0.0` exists as a published label, but it is provisional during the
CivicSuite release-recovery pass. Do not promote it as product-ready until the
recovery gates below are complete, post-merge CI is green, and broader suite
retest evidence re-earns that status.

## Recovery Gates

| Gate | Current status | Evidence |
| --- | --- | --- |
| Public product-ready claim freeze | Passing in branch | README, text README, user manual, docs landing page, changelog, and docs checks now describe `v1.0.0` as provisional. |
| Native WSL/Linux proof | Passing in branch | WSL selected `.venv-wsl/bin/python3`, reported platform `linux`, and completed `VERIFY-RELEASE: PASSED`. |
| Runtime install proof | Passing in branch | Fresh WSL editable install succeeded with the published CivicCore v1.0.0 release wheel and Hatch direct references enabled. |
| Security scan | Passing in branch | Tracked-file secret scan returned no matches. |
| Docs-source enforcement | Passing in branch | `scripts/verify-docs.sh` now blocks stale permit product-release claims. |
| Mock-vs-production labeling | Passing in branch | Existing docs distinguish local adversarial mocks, no legal advice, no permit approvals, and no live external calls by default. |
| Browser/user-flow QA | Passing in branch | Playwright checked `docs/index.html` at desktop and mobile widths; see `docs/browser-qa-civicpermit-release-recovery-summary.md`. |

## Current Evidence

- Focused Windows regression tests: `7 passed`.
- Native WSL release gate: `31 passed`; docs gate, placeholder import gate,
  ruff, build artifacts, and SHA256 generation passed.
- WSL fresh install: `python -m pip install -e .[dev]` succeeded in
  `.venv-wsl`.
- Browser QA: desktop `1440x1000` and mobile `390x844` passed with no console
  messages, no page errors, no horizontal overflow, and keyboard focus reaching
  the `recovery status` link.

## Sign-Off Boundary

This recovery status does not erase the existing `1.0.0` package version. It
changes the public posture: the current v1 label is provisional until runtime,
browser, security, documentation, and CI evidence re-earn product-ready status.
