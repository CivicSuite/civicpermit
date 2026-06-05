# CivicPermit Local Requirement Import

CivicPermit can load local municipal permit requirement CSV exports into the configured intake database. This is a local-first operator path; it does not call live permitting systems, GIS, LLMs, or vendor APIs.

## Database Target

Use the same SQLAlchemy URL that the runtime reads from `CIVICPERMIT_INTAKE_DB_URL`. The importer creates requirement tables if needed and does not seed sample requirements.

## CSV Contract

Required columns:

| Column | Purpose |
| --- | --- |
| `project_type_key` | Lookup keyword for applicant/staff questions, such as `adu`, `solar canopy`, or `commercial remodel`. |
| `requirement_id` | Local checklist identifier. Existing rows with the same identifier are updated. |
| `project_type` | Human-readable permit project type. |
| `title` | Human-readable checklist title. |
| `citation` | Public citation to the municipal intake guide, adopted code, policy, or staff checklist. |
| `required_materials` | Semicolon-separated material list. |
| `staff_note` | Staff routing or review note shown with the checklist. |

## Failure Behavior

- Missing required columns fail before any database writes.
- Empty required values fail before any database writes.
- `required_materials` must contain at least one semicolon-separated material.
- Existing `requirement_id` rows are updated, so repeated imports are idempotent.
- Sample requirements are not loaded into the target database by the importer.
