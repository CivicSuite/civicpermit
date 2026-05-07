# Security

CivicPermit is early-stage software. Current version: `0.1.2`. Do not deploy it as a system of record until a release explicitly says it is production-ready.

When `CIVICPERMIT_INTAKE_DB_URL` is configured, persisted intake create/read routes require `X-CivicPermit-Role: staff` from a trusted staff or service workflow. This header gate is a local release safeguard, not a replacement for production identity, tenant scoping, and audit logging.

Report suspected vulnerabilities privately to the project maintainer. Do not open public issues containing exploit details, secrets, or sensitive municipal data.
