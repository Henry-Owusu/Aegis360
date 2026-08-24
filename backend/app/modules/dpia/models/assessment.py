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

    title = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="draft"
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
