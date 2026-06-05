from __future__ import annotations

import pytest

from civicpermit.data_import import import_local_requirements
from civicpermit.persistence import PermitIntakeRepository


def test_local_requirement_import_loads_requirements_without_samples(tmp_path) -> None:
    db_url = f"sqlite:///{tmp_path / 'requirements.db'}"
    requirements_csv = tmp_path / "requirements.csv"
    requirements_csv.write_text(
        "\n".join(
            [
                (
                    "project_type_key,requirement_id,project_type,title,citation,"
                    "required_materials,staff_note"
                ),
                (
                    "solar canopy,permit-solar-canopy-1.0,solar-canopy,"
                    "Solar canopy intake checklist,Building Intake Guide Section 12,"
                    "Structural drawings.;Electrical one-line diagram.;Site plan.,"
                    "Route structural and electrical review before formal intake."
                ),
            ]
        ),
        encoding="utf-8",
    )

    summary = import_local_requirements(db_url=db_url, requirements_csv=requirements_csv)
    repository = PermitIntakeRepository(db_url=db_url, seed_defaults=False)
    requirement, source = repository.lookup_requirement_with_source(
        project_type="solar canopy",
        location_context="commercial parking lot",
    )

    assert summary.requirements == 1
    assert source == "configured"
    assert requirement.requirement_id == "permit-solar-canopy-1.0"
    assert requirement.required_materials == (
        "Structural drawings.",
        "Electrical one-line diagram.",
        "Site plan.",
    )
    assert len(repository.list_requirements()) == 1


def test_local_requirement_import_validates_csv_before_writing(tmp_path) -> None:
    db_url = f"sqlite:///{tmp_path / 'invalid.db'}"
    requirements_csv = tmp_path / "requirements.csv"
    requirements_csv.write_text(
        "\n".join(
            [
                (
                    "project_type_key,requirement_id,project_type,title,citation,"
                    "required_materials"
                ),
                (
                    "solar canopy,permit-solar-canopy-1.0,solar-canopy,"
                    "Solar canopy intake checklist,Building Intake Guide Section 12,"
                    "Structural drawings."
                ),
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="missing required columns: staff_note"):
        import_local_requirements(db_url=db_url, requirements_csv=requirements_csv)

    repository = PermitIntakeRepository(db_url=db_url, seed_defaults=False)
    assert repository.list_requirements() == ()


def test_local_requirement_import_updates_existing_requirement(tmp_path) -> None:
    db_url = f"sqlite:///{tmp_path / 'updated.db'}"
    requirements_csv = tmp_path / "requirements.csv"
    requirements_csv.write_text(
        "\n".join(
            [
                (
                    "project_type_key,requirement_id,project_type,title,citation,"
                    "required_materials,staff_note"
                ),
                (
                    "solar canopy,permit-solar-canopy-1.0,solar-canopy,"
                    "Solar canopy intake checklist,Building Intake Guide Section 12,"
                    "Structural drawings.;Electrical one-line diagram.,Initial note."
                ),
            ]
        ),
        encoding="utf-8",
    )
    import_local_requirements(db_url=db_url, requirements_csv=requirements_csv)
    requirements_csv.write_text(
        "\n".join(
            [
                (
                    "project_type_key,requirement_id,project_type,title,citation,"
                    "required_materials,staff_note"
                ),
                (
                    "solar canopy,permit-solar-canopy-1.0,solar-canopy,"
                    "Updated solar canopy checklist,Building Intake Guide Section 12,"
                    "Updated drawings.;Electrical one-line diagram.,Updated note."
                ),
            ]
        ),
        encoding="utf-8",
    )

    summary = import_local_requirements(db_url=db_url, requirements_csv=requirements_csv)
    repository = PermitIntakeRepository(db_url=db_url, seed_defaults=False)
    requirements = repository.list_requirements()

    assert summary.requirements == 1
    assert len(requirements) == 1
    assert requirements[0].title == "Updated solar canopy checklist"
    assert requirements[0].required_materials[0] == "Updated drawings."
