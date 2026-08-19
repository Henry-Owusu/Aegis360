from app.extensions.database import db
from app.modules.users.models import User

from app.modules.authentication.services.identity_provider import (
    MockIdentityProvider,
)
from app.modules.authentication.services.token_service import TokenService


class AuthService:

    @staticmethod
    def authenticate_mock(email: str) -> User:
        identity = MockIdentityProvider.authenticate(email)

        user = User.query.filter_by(
            entra_object_id=identity.object_id
        ).first()

        if not user:
            user = User(
                entra_object_id=identity.object_id,
                email=identity.email,
                first_name=identity.first_name,
                last_name=identity.last_name,
                is_active=True,
            )

            db.session.add(user)
            db.session.commit()

        if not user.is_active:
            raise ValueError("User account is inactive")

        return user

    @staticmethod
    def get_user_permissions(user: User) -> list[str]:
        permissions = set()

        for role in user.roles:
            for permission in role.permissions:
                permissions.add(permission.name)

        return sorted(permissions)

    @staticmethod
    def get_user_roles(user: User) -> list[str]:
        return sorted(role.name for role in user.roles)

    @staticmethod
    def create_mock_login_token(email: str):
        user = AuthService.authenticate_mock(email)

        token = TokenService.create_access_token(user)

        return user, token