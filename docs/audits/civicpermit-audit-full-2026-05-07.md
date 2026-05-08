# CivicPermit Audit-Full Recovery Packet

Date: 2026-05-07
Repo: `CivicSuite/civicpermit`
Branch: `recovery/civicpermit-release-truth-gates`
Mode: release-gate recovery cleanup

## 1. Executive Audit

Scope: CivicPermit local checkout and live `origin/main` parity at branch
baseline. Local `HEAD` and `origin/main` matched at
`fce5dfe02b320a7bc750f61289c4664a91092ce1`; the remote URL is
`https://github.com/CivicSuite/civicpermit.git` with no embedded token.

Overall verdict: CivicPermit already had the CivicCore release-wheel dependency
contract, but public docs promoted the v1 label too strongly and WSL release
verification could still prefer Windows Python. This branch freezes fresh
product-ready promotion, fixes WSL interpreter order, adds docs-source
guardrails, and will attach WSL/browser evidence before push.

Ship posture: do not promote CivicPermit as recertified product-ready until this
branch merges and post-merge CI is green.

Severity summary: Critical 1 fixed; Major 2 fixed; unresolved Blocker/Critical
0 in this branch-level recovery scope after verification.

Static audit confidence: high for release-script and docs changes.
Runtime sign-off confidence: medium-high after WSL install, WSL release gate,
and Playwright docs QA; final confidence depends on post-merge CI.

CI/workflow posture: CI exists and runs release verification; final status must
be checked after PR push and merge.

## 2. Audit Coverage Ledger

| Lane | Status | Evidence summary | Blocker |
| --- | --- | --- | --- |
| remote parity | Checked | `HEAD` and `origin/main` matched before edits. | None |
| local-vs-live commit truth | Checked | Divergence count was `0 0` at baseline. | None |
| CI/workflow presence | Checked | CI/release script present. | None |
| Windows install path | Partially checked | Focused local tests planned. | Full Windows release gate not required for this patch. |
| Linux or Unix install path | Checked | WSL native release gate passed. | None |
| platform parity verdict | Checked | Script now prefers `python3` before `python`. | None |
| first boot | Partially checked | Runtime endpoint tests cover FastAPI boot. | Full browser app flow remains for recertification. |
| required post-install steps | Checked | Release script handles package install/build verification. | None |
| migrations | Partially checked | Existing tests cover persistence paths. | No database rehearsal added here. |
| seed/bootstrap requirements | Partially checked | Existing sample data paths remain unchanged. | No new seed path. |
| runtime dependency and model requirements | Checked | CivicCore v1.0.0 release wheel; no live external calls by default. | None |
| first-boot dependency truth | Checked | Fresh WSL install passed with direct release-wheel dependency. | None |
| secrets and credential handling | Checked | Tracked-file secret scan returned no matches. | None |
| auth and session handling | Partially checked | Staff-only paths remain covered by existing tests. | Full auth browser QA remains. |
| authorization and role boundaries | Partially checked | Existing tests remain in suite. | Full role browser pass remains. |
| response-schema sensitive-data exposure | Partially checked | Existing tests remain in suite. | Not expanded here. |
| audit and compliance logging | Partially checked | Records export paths remain documented. | No new audit-log drill. |
| external and admin surfaces | Checked | Docs label local adversarial mocks and no live external calls by default. | None |
| connector implementation completeness | Partially checked | CivicZone/CivicCode context contracts not changed. | Full recertification remains. |
| connector docs truth | Checked | Mock-vs-production labeling retained. | None |
| background jobs and schedulers | Not applicable | No scheduler changed. | None |
| frontend critical journeys | Checked | Docs landing page Playwright pass completed. | None |
| loading states | Partially checked | Not changed by this branch. | Full UX recertification remains. |
| empty states | Partially checked | Not changed by this branch. | Full UX recertification remains. |
| error states | Partially checked | Not changed by this branch. | Full UX recertification remains. |
| partial states | Partially checked | Not changed by this branch. | Full UX recertification remains. |
| accessibility cues | Checked | First `Tab` reaches the recovery-status link. | None |
| docs truthfulness | Checked | Product-release wording replaced and banlist added. | None |
| version consistency | Checked | Version remains `1.0.0`; label is provisional. | None |
| release artifact consistency | Checked | WSL release gate built wheel, sdist, and `SHA256SUMS.txt`. | None |
| test realism | Checked | Regression tests added for interpreter order, dependency URL, and docs banlist. | None |
| runtime, build, and test verification | Checked | WSL release gate passed. | None |
| browser verification | Checked | Playwright desktop/mobile screenshots and summary added. | None |
| prior audit or verification challenge | Checked | Prior v1 product-ready posture challenged. | None |

## 3. Claim Verification Matrix

| Claim | Source | Verdict | Evidence |
| --- | --- | --- | --- |
| CivicPermit v1 is a published label. | `pyproject.toml`, docs | True | Version remains `1.0.0`. |
| CivicPermit is freshly product-ready. | Prior README/manual wording | False as a current claim | Docs now mark v1 provisional during recovery. |
| Fresh install can resolve CivicCore. | `pyproject.toml` | True in branch | WSL fresh install succeeded with the published CivicCore wheel and Hatch direct references enabled. |
| WSL release verification proves Linux. | Prior script order | True in branch | WSL selected `.venv-wsl/bin/python3`, platform `linux`, and passed release gate. |

## 4. What The Dev Team Needs To Do Now

### Must fix before ship

- None remaining before PR push; post-merge CI still gates final recovery status.

### Should fix this sprint

- `CI-001`: Push PR, wait for CI, merge only if green.

### Can defer if consciously accepted

- `UX-002`: Full application Playwright recertification across all public and
  staff states before any public product-ready announcement.

## 5. Next-Sprint Watchlist

Architecture: preserve CivicPermit as a CivicCore consumer and context consumer
of CivicZone/CivicCode without reverse dependency.
Security and compliance debt: expand staff-only intake browser checks.
UX debt: convert historical screenshot evidence to executable user-flow tests.
Docs debt: keep recovery labels synchronized across README/manual/docs.
Install/bootstrap debt: add fresh WSL first-boot app walkthrough.
Test debt: add regression tests for every release-gate failure class.
Operational and release debt: require post-merge CI proof before status changes.

## 6. Engineering Deep Dive

Verdict: release-script interpreter order was the primary engineering defect;
dependency metadata was already using the direct CivicCore release wheel.

### `[CRITICAL] REL-001 WSL release gate could select Windows Python`

- `Confidence`: High
- `Evidence type`: Runtime
- `Status`: Durable defect fixed

Why it matters:

A WSL release gate that runs Windows Python is not Linux evidence.

Evidence:

- `scripts/verify-release.sh` previously probed `python` before `python3`.
- The branch reverses that order and adds a regression test.

Blast radius:

- Every release verification run relying on WSL as Linux coverage.

Fix:

- Prefer native `python3` before `python`.

## 7. Security And Authorization Deep Dive

Verdict: tracked-file secret scan returned no matches. Strengths: no permit
approval or legal-advice behavior by default. Verification gaps: full browser
role pass remains for recertification.

## 8. UI/UX Deep Dive

Verdict: docs copy now sets accurate expectations and browser verification
passed. Strengths: docs landing page plainly says approvals, legal advice, live
GIS, live LLM calls, and system-of-record behavior are not shipped, and it links
to recovery status.

## 9. Product/PM Deep Dive

Verdict: product posture is now more honest: v1 exists as a label, not a fresh
announcement-ready certification. Verification gaps: broader suite retest.

## 10. Documentation Deep Dive

Verdict: stale permit product-release wording was real and fixed in branch.

### `[MAJOR] DOC-001 Public docs overclaimed v1 status`

- `Confidence`: High
- `Evidence type`: Static
- `Status`: Durable defect fixed

Why it matters:

Municipal users and auditors read release language as a trust claim.

Evidence:

- Current-facing docs now say the v1 label is under release-recovery review.

Blast radius:

- README, manuals, changelog, and docs landing page.

Fix:

- Replace product-release wording and add docs gate banlist entries.

## 11. Install / Bootstrap / Seeding Deep Dive

Verdict: fresh WSL install and native WSL release gate both pass. Verification
gaps: post-merge CI.

## 12. Version And Release Consistency Deep Dive

Verdict: version remains `1.0.0`; release posture is provisional. No version
bump was made because this is recovery truth labeling, not a new product claim.

## 13. Test Engineering Deep Dive

Verdict: regression tests now cover the failure classes.

### `[MAJOR] TEST-001 Docs and release gates lacked regression coverage for recovery truth`

- `Confidence`: High
- `Evidence type`: Static
- `Status`: Durable defect fixed

Why it matters:

Without tests, the same overclaim and WSL false-proof can return.

Evidence:

- `tests/test_runtime_foundation.py` now checks dependency URL, Hatch direct
  references, interpreter order, docs banlist, and current docs recovery
  language.

Blast radius:

- Future release maintenance.

Fix:

- Add regression tests.

## 14. Runtime QA Deep Dive

Verdict: `[AUDITOR-RUN]` WSL and Playwright evidence passed. Prior historical
QA remains treated as historical evidence only.

## 15. Cross-Cutting Synthesis

The root issue is the same suite-wide pattern: release labels outpaced current
proof. This branch narrows the claim, locks a gate around the exact wording, and
fixes platform proof.

## 16. Verification Gaps And Sign-Off Limits

- Post-merge CI: required after PR merge.
- Full product recertification: outside this branch; required before public
  product-ready announcement.
