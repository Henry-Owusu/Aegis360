from datetime import datetime, timedelta, timezone

import jwt

from flask import current_app


class TokenService:

    @staticmethod
    def create_access_token(user):
        now = datetime.now(timezone.utc)

        expires_at = now + timedelta(
            minutes=current_app.config["JWT_EXPIRATION_MINUTES"]
        )

        payload = {
            "sub": user.id,
            "email": user.email,
            "iat": now,
            "exp": expires_at,
        }

        return jwt.encode(
            payload,
            current_app.config["JWT_SECRET_KEY"],
            algorithm=current_app.config["JWT_ALGORITHM"],
        )

    @staticmethod
    def decode_access_token(token):
        return jwt.decode(
            token,
            current_app.config["JWT_SECRET_KEY"],
            algorithms=[
                current_app.config["JWT_ALGORITHM"]
            ],
        )
