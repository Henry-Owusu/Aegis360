from flask import Flask
from flask_migrate import Migrate

from app.config.settings import Config
from app.extensions.database import db
from app.api.health import health_bp

from app.modules.users.models import User

from app.modules.authorization.models import (
    Role,
    Permission,
    UserRole,
    RolePermission,
)

from app.modules.authentication.routes import auth_bp

migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)

    return app