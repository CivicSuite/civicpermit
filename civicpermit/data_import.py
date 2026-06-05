from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

from civicpermit.persistence import PermitIntakeRepository
from civicpermit.requirement_lookup import PermitRequirement


REQUIREMENT_COLUMNS = {
    "project_type_key",
    "requirement_id",
    "project_type",
    "title",
    "citation",
    "required_materials",
    "staff_note",
}


@dataclass(frozen=True)
class ImportSummary:
    requirements: int = 0


def import_local_requirements(*, db_url: str, requirements_csv: Path) -> ImportSummary:
    """Validate and import local permit requirement CSV rows into CivicPermit."""

    records = [
        (
            _required(row, "project_type_key"),
            PermitRequirement(
                requirement_id=_required(row, "requirement_id"),
                project_type=_required(row, "project_type"),
                title=_required(row, "title"),
                citation=_required(row, "citation"),
                required_materials=_required_materials(row, requirements_csv, index),
                staff_note=_required(row, "staff_note"),
            ),
        )
        for index, row in _read_rows(requirements_csv)
    ]

    repository = PermitIntakeRepository(db_url=db_url, seed_defaults=False)
    for project_type_key, requirement in records:
        repository.upsert_requirement(project_type_key=project_type_key, requirement=requirement)
    return ImportSummary(requirements=len(records))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Import local municipal permit requirement CSV rows into CivicPermit."
    )
    parser.add_argument(
        "--db-url",
        required=True,
        help="SQLAlchemy database URL for CivicPermit requirement records.",
    )
    parser.add_argument(
        "--requirements-csv",
        required=True,
        type=Path,
        help="CSV with local permit requirement rows.",
    )
    args = parser.parse_args(argv)

    summary = import_local_requirements(
        db_url=args.db_url,
        requirements_csv=args.requirements_csv,
    )
    print(f"CivicPermit import complete: {summary.requirements} requirements.")
    return 0


def _read_rows(path: Path) -> list[tuple[int, dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing = sorted(REQUIREMENT_COLUMNS - fieldnames)
        if missing:
            raise ValueError(f"{path} is missing required columns: {', '.join(missing)}")
        rows = list(reader)
    for index, row in enumerate(rows, start=2):
        for column in REQUIREMENT_COLUMNS:
            if row.get(column, "").strip() == "":
                raise ValueError(f"{path}:{index} has an empty required value for {column}")
        _required_materials(row, path, index)
    return list(enumerate(rows, start=2))


def _required(row: dict[str, str], column: str) -> str:
    return row[column].strip()


def _required_materials(row: dict[str, str], path: Path, index: int) -> tuple[str, ...]:
    materials = tuple(
        material.strip()
        for material in row["required_materials"].split(";")
        if material.strip()
    )
    if not materials:
        raise ValueError(f"{path}:{index} has an empty required value for required_materials")
    return materials


if __name__ == "__main__":
    raise SystemExit(main())
