from flask import Blueprint, jsonify

from app.extensions.database import db
# pyrefly: ignore [missing-import]
from sqlalchemy import text


health_bp = Blueprint("health", __name__)


@health_bp.route("/api/health", methods=["GET"])
def health():
    try:
        db.session.execute(text("SELECT 1"))

        return jsonify({
            "status": "ok",
            "database": "connected"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "database": "disconnected",
            "error": str(e)
        }), 500