import uuid

from app.extensions.database import db


class DPIAQuestion(db.Model):
    __tablename__ = "dpia_questions"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # Can be 'basic_data', 'screening', 'full_pia'
    section = db.Column(
        db.String(50),
        nullable=False
    )

    # Re-using section_title for the internal grouping within the section
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
        default=True
    )

    display_order = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    conditional_logic = db.Column(
        db.JSON,
        nullable=True
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    responses = db.relationship(
        "DPIAResponse",
        backref="question"
    )

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"<DPIAQuestion {self.section}:{self.question_number} - {self.question_text[:20]}>"