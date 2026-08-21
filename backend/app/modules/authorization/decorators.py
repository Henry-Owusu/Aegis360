from functools import wraps

from flask import jsonify, request

from app.modules.authentication.services.token_service import TokenService
from app.modules.users.models import User


def require_permission(permission_name):
    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return jsonify({
                    "error": "Authorization header is required"
                }), 401

            if not auth_header.startswith("Bearer "):
                return jsonify({
                    "error": "Invalid authorization header"
                }), 401

            token = auth_header.split(" ", 1)[1]

            try:
                payload = TokenService.decode_access_token(token)

            except Exception:
                return jsonify({
                    "error": "Invalid or expired token"
                }), 401

            user = User.query.get(payload.get("sub"))

            if not user:
                return jsonify({
                    "error": "User not found"
                }), 401

            if not user.is_active:
                return jsonify({
                    "error": "User account is inactive"
                }), 403

            user_permissions = {
                permission.name
                for role in user.roles
                for permission in role.permissions
            }

            if permission_name not in user_permissions:
                return jsonify({
                    "error": "Forbidden",
                    "message": (
                        f"Permission required: {permission_name}"
                    )
                }), 403

            return function(*args, **kwargs)

        return wrapper

    return decorator
