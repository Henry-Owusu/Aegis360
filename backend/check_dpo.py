from app import create_app
from app.extensions.database import db
from app.modules.users.models import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(email='dpo@aegis360.com').first()
    if user:
        print(f"User: {user.email}")
        print(f"Roles: {[r.name for r in user.roles]}")
    else:
        print("User not found.")
