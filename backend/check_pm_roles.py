from app import create_app
from app.extensions.database import db
from app.modules.users.models import User

app = create_app()
with app.app_context():
    pm = User.query.filter_by(email='pm@aegis360.com').first()
    print("PM roles:", [r.name for r in pm.roles])

