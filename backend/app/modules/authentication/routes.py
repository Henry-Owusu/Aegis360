from flask import Blueprint, jsonify, request, g

from app.modules.authentication.services.auth_service import AuthService
from app.modules.authentication.middleware.auth import require_auth

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth",
)


@auth_bp.post("/mock-login")
def mock_login():
    data = request.get_json() or {}

    email = data.get("email")

    if not email:
        return jsonify({
            "error": "Email is required"
        }), 400

    try:
        user, token = AuthService.create_mock_login_token(email)

        return jsonify({
            "message": "Mock login successful",
            "access_token": token,
            "token_type": "Bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_active": user.is_active,
            },
            "roles": AuthService.get_user_roles(user),
            "permissions": AuthService.get_user_permissions(user),
        }), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 401


@auth_bp.get("/me")
@require_auth
def get_current_user():

    user = g.current_user

    return jsonify({
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
        },
        "roles": AuthService.get_user_roles(user),
        "permissions": AuthService.get_user_permissions(user),
    }), 200