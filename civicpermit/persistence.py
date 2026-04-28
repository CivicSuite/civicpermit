from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import Engine, create_engine

from civicpermit.intake_review import review_intake_readiness
from civicpermit.requirement_lookup import REQUIREMENTS, PermitRequirement, lookup_permit_requirement


metadata = sa.MetaData()

permit_requirement_records = sa.Table(
    "permit_requirement_records",
    metadata,
    sa.Column("requirement_id", sa.String(160), primary_key=True),
    sa.Column("project_type_key", sa.String(160), nullable=False),
    sa.Column("project_type", sa.String(255), nullable=False),
    sa.Column("title", sa.String(500), nullable=False),
    sa.Column("citation", sa.String(500), nullable=False),
    sa.Column("required_materials", sa.JSON(), nullable=False),
    sa.Column("staff_note", sa.Text(), nullable=False),
    sa.Column("disclaimer", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    schema="civicpermit",
)

intake_review_records = sa.Table(
    "intake_review_records",
    metadata,
    sa.Column("intake_id", sa.String(36), primary_key=True),
    sa.Column("project_type", sa.String(255), nullable=False),
    sa.Column("proposal", sa.Text(), nullable=False),
    sa.Column("status", sa.String(120), nullable=False),
    sa.Column("missing_or_unclear", sa.JSON(), nullable=False),
    sa.Column("next_step", sa.Text(), nullable=False),
    sa.Column("disclaimer", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civicpermit",
)


@dataclass(frozen=True)
class StoredIntakeReview:
    intake_id: str
    project_type: str
    proposal: str
    status: str
    missing_or_unclear: tuple[str, ...]
    next_step: str
    disclaimer: str
    created_at: datetime


class PermitIntakeRepository:
    """SQLAlchemy-backed permit requirement and intake-readiness records."""

    def __init__(self, *, db_url: str | None = None, engine: Engine | None = None, seed_defaults: bool = True) -> None:
        base_engine = engine or create_engine(db_url or "sqlite+pysqlite:///:memory:", future=True)
        if base_engine.dialect.name == "sqlite":
            self.engine = base_engine.execution_options(schema_translate_map={"civicpermit": None})
        else:
            self.engine = base_engine
            with self.engine.begin() as connection:
                connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS civicpermit"))
        metadata.create_all(self.engine)
        if seed_defaults:
            self.seed_requirements(REQUIREMENTS.items())

    def seed_requirements(self, requirements: Iterable[tuple[str, PermitRequirement]]) -> None:
        now = datetime.now(UTC)
        with self.engine.begin() as connection:
            for project_type_key, requirement in requirements:
                exists = connection.execute(
                    sa.select(permit_requirement_records.c.requirement_id).where(
                        permit_requirement_records.c.requirement_id == requirement.requirement_id
                    )
                ).first()
                if exists is not None:
                    continue
                connection.execute(
                    permit_requirement_records.insert().values(
                        requirement_id=requirement.requirement_id,
                        project_type_key=project_type_key.casefold(),
                        project_type=requirement.project_type,
                        title=requirement.title,
                        citation=requirement.citation,
                        required_materials=list(requirement.required_materials),
                        staff_note=requirement.staff_note,
                        disclaimer=requirement.disclaimer,
                        created_at=now,
                        updated_at=now,
                    )
                )

    def lookup_requirement(self, *, project_type: str, location_context: str = "") -> PermitRequirement:
        normalized = project_type.strip().casefold()
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(permit_requirement_records).where(
                    sa.or_(
                        permit_requirement_records.c.project_type_key == normalized,
                        sa.func.lower(permit_requirement_records.c.requirement_id) == normalized,
                    )
                )
            ).mappings().first()
        if row is not None:
            return _row_to_requirement(row)
        return lookup_permit_requirement(project_type=project_type, location_context=location_context)

    def create_intake_review(self, *, proposal: str, project_type: str) -> StoredIntakeReview:
        review = review_intake_readiness(proposal=proposal, project_type=project_type)
        stored = StoredIntakeReview(
            intake_id=str(uuid4()),
            project_type=review.project_type,
            proposal=proposal,
            status=review.status,
            missing_or_unclear=review.missing_or_unclear,
            next_step=review.next_step,
            disclaimer=review.disclaimer,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(
                intake_review_records.insert().values(
                    intake_id=stored.intake_id,
                    project_type=stored.project_type,
                    proposal=stored.proposal,
                    status=stored.status,
                    missing_or_unclear=list(stored.missing_or_unclear),
                    next_step=stored.next_step,
                    disclaimer=stored.disclaimer,
                    created_at=stored.created_at,
                )
            )
        return stored

    def get_intake_review(self, intake_id: str) -> StoredIntakeReview | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(intake_review_records).where(intake_review_records.c.intake_id == intake_id)
            ).mappings().first()
        if row is None:
            return None
        return _row_to_intake(row)


def _row_to_requirement(row: object) -> PermitRequirement:
    data = dict(row)
    return PermitRequirement(
        requirement_id=data["requirement_id"],
        project_type=data["project_type"],
        title=data["title"],
        citation=data["citation"],
        required_materials=tuple(data["required_materials"]),
        staff_note=data["staff_note"],
        disclaimer=data["disclaimer"],
    )


def _row_to_intake(row: object) -> StoredIntakeReview:
    data = dict(row)
    return StoredIntakeReview(
        intake_id=data["intake_id"],
        project_type=data["project_type"],
        proposal=data["proposal"],
        status=data["status"],
        missing_or_unclear=tuple(data["missing_or_unclear"]),
        next_step=data["next_step"],
        disclaimer=data["disclaimer"],
        created_at=data["created_at"],
    )
