from flask import Flask
from flask_cors import CORS
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
from app.modules.dpia.models import (
    DPIAAssessment,
    DPIAFullPIA,
    DPIAQuestion,
    DPIAResponse,
)
from app.modules.dpia.routes import (
    dpia_bp
)
from app.modules.users.routes import users_bp

migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app, origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://127.0.0.1:5175"], supports_credentials=True)

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dpia_bp)
    app.register_blueprint(users_bp)

    return app
