import uuid

from datetime import datetime, timezone

from app.extensions.database import db


class Role(db.Model):

    __tablename__ = "roles"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    name = db.Column(
        db.String(100),
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

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    permissions = db.relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles"
    )

    users = db.relationship(
        "User",
        secondary="user_roles",
        back_populates="roles"
    )