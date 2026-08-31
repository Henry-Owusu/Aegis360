from app import create_app
from app.extensions.database import db
from app.modules.users.models import User
from app.modules.authorization.models import Role

app = create_app()
with app.app_context():
    pm = User.query.filter_by(email='pm@aegis360.com').first()
    if not pm:
        pm = User(email='pm@aegis360.com', first_name='Project', last_name='Manager')
        db.session.add(pm)
        db.session.commit()
        
    role = Role.query.filter_by(name='PM').first()
    if role not in pm.roles:
        pm.roles.append(role)
        db.session.commit()
        print("Assigned PM to pm@aegis360.com")
