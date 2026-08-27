import uuid

from datetime import datetime, timezone

from app.extensions.database import db


class DPIAScreening(db.Model):

    __tablename__ = "dpia_screenings"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    assessment_id = db.Column(
        db.String(36),
        db.ForeignKey("dpia_assessments.id"),
        unique=True,
        nullable=False
    )


    # Personal Data

    involves_personal_data = db.Column(
        db.Boolean,
        nullable=True
    )

    # Personal Data Categories
    # Stored as JSON for now because each question supports
    # multiple selections.

    personal_data_subject_types = db.Column(
        db.JSON,
        nullable=True
    )

    personal_data_categories = db.Column(
        db.JSON,
        nullable=True
    )

    sensitive_personal_data_categories = db.Column(
        db.JSON,
        nullable=True
    )

    other_personal_data = db.Column(
        db.Text,
        nullable=True
    )

    # Data Subject Locations
    data_subject_locations = db.Column(
        db.JSON,
        nullable=True
    )

    data_subject_specific_countries = db.Column(
        db.Text,
        nullable=True
    )


    # Volume / Access


    approximate_users_with_access = db.Column(
        db.Integer,
        nullable=True
    )

    approximate_records_per_year = db.Column(
        db.Integer,
        nullable=True
    )


    # System Use Locations


    system_use_locations = db.Column(
        db.JSON,
        nullable=True
    )

    system_use_specific_countries = db.Column(
        db.Text,
        nullable=True
    )


    # Hosting

    system_hosting_locations = db.Column(
        db.JSON,
        nullable=True
    )

    system_hosting_specific_countries = db.Column(
        db.Text,
        nullable=True
    )

    system_host = db.Column(
        db.String(255),
        nullable=True
    )

 
    # Support
 

    system_support_types = db.Column(
        db.JSON,
        nullable=True
    )

    support_locations = db.Column(
        db.JSON,
        nullable=True
    )

    support_specific_countries = db.Column(
        db.Text,
        nullable=True
    )


    # Third Party Access

    third_party_access = db.Column(
        db.Boolean,
        nullable=True
    )

    third_party_access_explanation = db.Column(
        db.Text,
        nullable=True
    )

    # Screening Outcome

    # Risk calculation is intentionally NOT implemented yet.
    # This field is reserved for the future screening engine.

    risk_tier = db.Column(
        db.String(50),
        nullable=True
    )

    full_pia_required = db.Column(
        db.Boolean,
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
        back_populates="screening"
    )

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

