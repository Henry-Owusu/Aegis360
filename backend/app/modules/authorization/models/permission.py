import uuid

from datetime import datetime, timezone

from app.extensions.database import db


class Permission(db.Model):

    __tablename__ = "permissions"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    name = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.String(255),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    roles = db.relationship(
        "Role",
        secondary="role_permissions",
        back_populates="permissions"
    )

    def __init__(self, name: str | None = None, description: str | None = None, **kwargs):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        for key, value in kwargs.items():
            setattr(self, key, value)