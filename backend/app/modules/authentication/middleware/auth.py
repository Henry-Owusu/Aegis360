from functools import wraps

from flask import request, jsonify, g

from app.modules.authentication.services.token_service import TokenService
from app.modules.users.models import User


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "error": "Authorization header is required"
            }), 401

        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({
                "error": "Invalid Authorization header"
            }), 401

        token = parts[1]

        try:
            payload = TokenService.decode_access_token(token)

        except Exception:
            return jsonify({
                "error": "Invalid or expired access token"
            }), 401

        user_id = payload.get("sub")

        if not user_id:
            return jsonify({
                "error": "Invalid token payload"
            }), 401

        user = User.query.get(user_id)

        if not user:
            return jsonify({
                "error": "User not found"
            }), 401

        if not user.is_active:
            return jsonify({
                "error": "User account is inactive"
            }), 403

        g.current_user = user

        return f(*args, **kwargs)

    return decorated
