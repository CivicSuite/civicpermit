# Security

CivicPermit Current version: 0.2.2. This is a narrow truth-repair release with no functional upgrade. The previous v1.0.0 release was published in error and does not prove public-use readiness. It supports permit pre-application and intake-readiness scaffold workflows, but it is not a permitting system of record.

When `CIVICPERMIT_INTAKE_DB_URL` is configured, persisted intake, staff review queue, and staff summary routes require `CIVICPERMIT_STAFF_API_KEY`, `X-CivicPermit-Role: staff`, and a matching `X-CivicPermit-Staff-Key` from a trusted staff workflow. CivicPermit uses CivicCore `staff_key_gate` for timing-safe key comparison. This local API-key gate is a release safeguard, not a replacement for production identity, tenant scoping, and audit logging.

Report suspected vulnerabilities privately to the project maintainer. Do not open public issues containing exploit details, secrets, or sensitive municipal data.
