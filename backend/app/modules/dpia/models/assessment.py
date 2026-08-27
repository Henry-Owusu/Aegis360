import uuid

from datetime import datetime, timezone

from app.extensions.database import db


class DPIAAssessment(db.Model):

    __tablename__ = "dpia_assessments"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # ============================================================
    # BASIC DATA
    # ============================================================

    project_manager = db.Column(
        db.String(255),
        nullable=False
    )

    department_function_agency = db.Column(
        db.String(255),
        nullable=True
    )

    area_ministry = db.Column(
        db.String(255),
        nullable=True
    )

    region = db.Column(
        db.String(255),
        nullable=True
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    nature_of_change = db.Column(
        db.JSON,
        nullable=False
    )

    other_nature_of_change = db.Column(
        db.String(500),
        nullable=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    implementation_timescales = db.Column(
        db.Text,
        nullable=True
    )

    # ============================================================
    # WORKFLOW
    # ============================================================

    status = db.Column(
        db.String(50),
        nullable=False,
        default="draft"
    )

    dps_review_decision = db.Column(
        db.String(50),
        nullable=True
    )

    dps_review_comment = db.Column(
        db.Text,
        nullable=True
    )

    dps_reviewed_by = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=True
    )

    dps_reviewed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    created_by = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # ============================================================
    # RELATIONSHIPS
    # ============================================================

    screening = db.relationship(
        "DPIAScreening",
        back_populates="assessment",
        uselist=False,
        cascade="all, delete-orphan"
    )