from functools import wraps

from flask import jsonify

from app.modules.authorization.services.authorization_service import (
    AuthorizationService,
)


def require_permission(permission_name):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            try:
                user = AuthorizationService.get_current_user()

            except PermissionError as error:
                return jsonify({
                    "error": "Forbidden",
                    "message": str(error),
                }), 403

            except ValueError as error:
                return jsonify({
                    "error": str(error),
                }), 401

            if not AuthorizationService.has_permission(
                user,
                permission_name
            ):
                return jsonify({
                    "error": "Forbidden",
                    "message": (
                        f"Permission required: {permission_name}"
                    ),
                }), 403

            return function(*args, **kwargs)

        return wrapper

    return decorator


def require_role(role_name):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            try:
                user = AuthorizationService.get_current_user()

            except PermissionError as error:
                return jsonify({
                    "error": "Forbidden",
                    "message": str(error),
                }), 403

            except ValueError as error:
                return jsonify({
                    "error": str(error),
                }), 401

            if not AuthorizationService.has_role(
                user,
                role_name
            ):
                return jsonify({
                    "error": "Forbidden",
                    "message": f"Role required: {role_name}",
                }), 403

            return function(*args, **kwargs)

        return wrapper

    return decorator


def require_any_permission(*permission_names):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            try:
                user = AuthorizationService.get_current_user()

            except PermissionError as error:
                return jsonify({
                    "error": "Forbidden",
                    "message": str(error),
                }), 403

            except ValueError as error:
                return jsonify({
                    "error": str(error),
                }), 401

            user_permissions = (
                AuthorizationService.get_user_permissions(user)
            )

            if not user_permissions.intersection(permission_names):
                return jsonify({
                    "error": "Forbidden",
                    "message": (
                        "One of these permissions is required: "
                        + ", ".join(permission_names)
                    ),
                }), 403

            return function(*args, **kwargs)

        return wrapper

    return decorator