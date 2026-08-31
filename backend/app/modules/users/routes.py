from flask import Blueprint, jsonify, request, g

from app.extensions.database import db
from app.modules.authentication.middleware.auth import require_auth
from app.modules.authorization.decorators import require_role
from app.modules.users.models import User
from app.modules.authorization.models import Role

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


# ── List all users ────────────────────────────────────────────────────────────

@users_bp.get("")
@require_auth
@require_role("System Administrator")
def list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify({
        "users": [
            {
                "id": u.id,
                "email": u.email,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "is_active": u.is_active,
                "roles": [r.name for r in u.roles],
                "created_at": u.created_at.isoformat(),
            }
            for u in users
        ],
        "total": len(users)
    }), 200


# ── Get single user ───────────────────────────────────────────────────────────

@users_bp.get("/<user_id>")
@require_auth
@require_role("System Administrator")
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
        "roles": [r.name for r in user.roles],
        "created_at": user.created_at.isoformat(),
    }), 200


# ── Toggle user active status ─────────────────────────────────────────────────

@users_bp.patch("/<user_id>/toggle-status")
@require_auth
@require_role("System Administrator")
def toggle_status(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Prevent admin from deactivating themselves
    if user.id == g.current_user.id:
        return jsonify({"error": "You cannot deactivate your own account"}), 400

    user.is_active = not user.is_active
    db.session.commit()

    return jsonify({
        "id": user.id,
        "is_active": user.is_active,
        "message": f"User {'activated' if user.is_active else 'deactivated'} successfully"
    }), 200


# ── Assign role to user ───────────────────────────────────────────────────────

@users_bp.post("/<user_id>/roles")
@require_auth
@require_role("System Administrator")
def assign_role(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json() or {}
    role_name = data.get("role")
    if not role_name:
        return jsonify({"error": "role is required"}), 400

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return jsonify({"error": f"Role '{role_name}' not found"}), 404

    if role not in user.roles:
        user.roles.append(role)
        db.session.commit()

    return jsonify({
        "message": f"Role '{role_name}' assigned to {user.email}",
        "roles": [r.name for r in user.roles]
    }), 200


# ── Remove role from user ─────────────────────────────────────────────────────

@users_bp.delete("/<user_id>/roles/<role_name>")
@require_auth
@require_role("System Administrator")
def remove_role(user_id, role_name):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    role = Role.query.filter_by(name=role_name).first()
    if role and role in user.roles:
        user.roles.remove(role)
        db.session.commit()

    return jsonify({
        "message": f"Role '{role_name}' removed from {user.email}",
        "roles": [r.name for r in user.roles]
    }), 200


# ── List all roles (for dropdowns) ────────────────────────────────────────────

@users_bp.get("/meta/roles")
@require_auth
@require_role("System Administrator")
def list_roles():
    roles = Role.query.order_by(Role.name).all()
    return jsonify({
        "roles": [{"id": r.id, "name": r.name, "description": r.description} for r in roles]
    }), 200
