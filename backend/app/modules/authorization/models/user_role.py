from app.extensions.database import db


class UserRole(db.Model):
    __tablename__ = "user_roles"

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        primary_key=True
    )

    role_id = db.Column(
        db.String(36),
        db.ForeignKey("roles.id"),
        primary_key=True
    )