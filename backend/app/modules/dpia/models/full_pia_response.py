import uuid

from datetime import datetime, timezone

from app.extensions.database import db


class DPIAFullPIAResponse(db.Model):
    __tablename__ = "dpia_full_pia_responses"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    full_pia_id = db.Column(
        db.String(36),
        db.ForeignKey("dpia_full_pias.id"),
        nullable=False
    )

    question_id = db.Column(
        db.String(36),
        db.ForeignKey("dpia_full_pia_questions.id"),
        nullable=False
    )

    answer = db.Column(
        db.JSON,
        nullable=True
    )

    answered_by = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=True
    )

    answered_at = db.Column(
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

    full_pia = db.relationship(
        "DPIAFullPIA",
        back_populates="responses"
    )

    question = db.relationship(
        "DPIAFullPIAQuestion",
        back_populates="responses"
    )

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)