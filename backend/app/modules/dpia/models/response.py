import uuid

from datetime import datetime, timezone

from app.extensions.database import db


class DPIAResponse(db.Model):
    __tablename__ = "dpia_responses"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    assessment_id = db.Column(
        db.String(36),
        db.ForeignKey("dpia_assessments.id"),
        nullable=False
    )

    question_id = db.Column(
        db.String(36),
        db.ForeignKey("dpia_questions.id"),
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

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)