import uuid

from app.extensions.database import db


class DPIAFullPIAQuestion(db.Model):
    __tablename__ = "dpia_full_pia_questions"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    section = db.Column(
        db.Integer,
        nullable=False
    )

    section_title = db.Column(
        db.String(255),
        nullable=False
    )

    question_number = db.Column(
        db.String(20),
        nullable=False
    )

    question_text = db.Column(
        db.Text,
        nullable=False
    )

    guidance = db.Column(
        db.Text,
        nullable=True
    )

    answer_type = db.Column(
        db.String(50),
        nullable=False
    )

    options = db.Column(
        db.JSON,
        nullable=True
    )

    required = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    display_order = db.Column(
        db.Integer,
        nullable=False
    )

    conditional_logic = db.Column(
        db.JSON,
        nullable=True
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    responses = db.relationship(
        "DPIAFullPIAResponse",
        back_populates="question"
    )

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)