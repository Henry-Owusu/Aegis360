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

    # Core System Data
    
    project_manager = db.Column(
        db.String(255),
        nullable=False
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="Draft"
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

    # Relationships
    full_pia = db.relationship(
        "DPIAFullPIA",
        back_populates="assessment",
        uselist=False,
        cascade="all, delete-orphan"
    )
    
    responses = db.relationship(
        "DPIAResponse",
        backref="assessment",
        cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)