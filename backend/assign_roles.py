from app import create_app
from app.extensions.database import db
from app.modules.users.models import User
from app.modules.authorization.models import Role

app = create_app()
with app.app_context():
    def assign_role(email, role_name):
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"User {email} not found. Login once to create them.")
            return
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            print(f"Role {role_name} not found.")
            return
        if role not in user.roles:
            user.roles.append(role)
            print(f"Assigned {role_name} to {email}")
            
    assign_role('dpo@aegis360.com', 'DPO')
    assign_role('pm@aegis360.com', 'PM')
    assign_role('admin@aegis360.com', 'System Administrator')
    assign_role('approver@aegis360.com', 'Approver')
    assign_role('auditor@aegis360.com', 'Auditor')
    
    db.session.commit()
    print("Done")
