from __future__ import annotations

import argparse

from civicpermit.persistence import PermitIntakeRepository


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check and initialize the local CivicPermit intake database schema."
    )
    parser.add_argument(
        "--db-url",
        required=True,
        help="SQLAlchemy database URL used by CIVICPERMIT_INTAKE_DB_URL.",
    )
    args = parser.parse_args()

    repository = PermitIntakeRepository(db_url=args.db_url, seed_defaults=False)
    try:
        status = repository.schema_status()
    finally:
        repository.engine.dispose()

    ready = "ready" if status.ready else "not ready"
    missing = ", ".join(status.missing_tables) if status.missing_tables else "none"
    version = status.schema_version or "none"
    print(
        "CivicPermit schema "
        f"{ready}: version={version}; expected={status.expected_schema_version}; "
        f"dialect={status.dialect}; missing_tables={missing}."
    )


if __name__ == "__main__":
    main()
