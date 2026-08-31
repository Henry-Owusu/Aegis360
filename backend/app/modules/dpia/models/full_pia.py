import uuid

from datetime import datetime, timezone

from app.extensions.database import db


class DPIAFullPIA(db.Model):
    __tablename__ = "dpia_full_pias"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    assessment_id = db.Column(
        db.String(36),
        db.ForeignKey("dpia_assessments.id"),
        nullable=False,
        unique=True
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="draft"
    )

    started_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    submitted_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
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

    assessment = db.relationship(
        "DPIAAssessment",
        back_populates="full_pia"
    )

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)