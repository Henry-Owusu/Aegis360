from flask import request

from app.modules.authentication.services.token_service import TokenService
from app.modules.users.models import User


class AuthorizationService:

    @staticmethod
    def get_current_user():
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise ValueError("Authorization header is required")

        if not auth_header.startswith("Bearer "):
            raise ValueError("Invalid authorization header")

        token = auth_header.split(" ", 1)[1].strip()

        if not token:
            raise ValueError("Bearer token is required")

        try:
            payload = TokenService.decode_access_token(token)
        except Exception:
            raise ValueError("Invalid or expired token")

        user_id = payload.get("sub")

        if not user_id:
            raise ValueError("Invalid token payload")

        user = User.query.get(user_id)

        if not user:
            raise ValueError("User not found")

        if not user.is_active:
            raise PermissionError("User account is inactive")

        return user

    @staticmethod
    def get_user_permissions(user):
        return {
            permission.name
            for role in user.roles
            for permission in role.permissions
        }

    @staticmethod
    def get_user_roles(user):
        return {
            role.name
            for role in user.roles
        }

    @staticmethod
    def has_permission(user, permission_name):
        return permission_name in AuthorizationService.get_user_permissions(user)

    @staticmethod
    def has_role(user, role_name):
        return role_name in AuthorizationService.get_user_roles(user)
