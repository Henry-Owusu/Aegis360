from app import create_app
from app.extensions.database import db

from app.modules.authorization.models import Role, Permission


ROLES = [
    {
        "name": "System Administrator",
        "description": "Full system administration access",
    },
    {
        "name": "DPO",
        "description": "Data Protection Officer",
    },
    {
        "name": "DPS",
        "description": "Data Protection Specialist",
    },
    {
        "name": "Auditor",
        "description": "Audit and read-only access",
    },
    {
        "name": "PM",
        "description": "Project Manager",
    },
    {
        "name": "Approver",
        "description": "Legal approval and review",
    },
]


PERMISSIONS = [
    {
        "name": "assessment.view",
        "description": "View DPIA assessments.",
    },
    {
        "name": "assessment.create",
        "description": "Create DPIA assessments.",
    },
    {
        "name": "assessment.edit",
        "description": "Edit DPIA assessments.",
    },
    {
        "name": "assessment.delete",
        "description": "Delete DPIA assessments.",
    },
    {
        "name": "assessment.approve",
        "description": "Approve DPIA assessments.",
    },
    {
        "name": "risk.view",
        "description": "View DPIA risks.",
    },
    {
        "name": "risk.create",
        "description": "Create DPIA risks.",
    },
    {
        "name": "risk.edit",
        "description": "Edit DPIA risks.",
    },
    {
        "name": "risk.manage",
        "description": "Manage DPIA risks.",
    },
    {
        "name": "report.view",
        "description": "View reports.",
    },
    {
        "name": "report.create",
        "description": "Create reports.",
    },
    {
        "name": "report.export",
        "description": "Export reports.",
    },
    {
        "name": "user.view",
        "description": "View users.",
    },
    {
        "name": "user.manage",
        "description": "Manage users.",
    },
    {
        "name": "role.view",
        "description": "View roles.",
    },
    {
        "name": "role.manage",
        "description": "Manage roles and permissions.",
    },
]

ROLE_PERMISSIONS = {
    "System Administrator": [
        "assessment.view",
        "assessment.create",
        "assessment.edit",
        "assessment.delete",
        "assessment.approve",
        "risk.view",
        "risk.create",
        "risk.edit",
        "risk.manage",
        "report.view",
        "report.create",
        "report.export",
        "user.view",
        "user.manage",
        "role.view",
        "role.manage",
    ],

    "DPO": [
        "assessment.view",
        "assessment.create",
        "assessment.edit",
        "assessment.approve",
        "risk.view",
        "risk.create",
        "risk.edit",
        "risk.manage",
        "report.view",
        "report.create",
        "report.export",
    ],

    "DPS": [
        "assessment.view",
        "assessment.create",
        "assessment.edit",
        "risk.view",
        "risk.create",
        "risk.edit",
        "report.view",
        "report.create",
        "report.export",
    ],

    "Auditor": [
        "assessment.view",
        "risk.view",
        "report.view",
    ],

    "PM": [
        "assessment.view",
        "assessment.create",
        "assessment.edit",
        "risk.view",
        "risk.create",
        "report.view",
        "report.create",
        "report.export",
    ],

    "Approver": [
        "assessment.view",
        "assessment.approve",
        "risk.view",
        "report.view",
    ],
}


def seed_roles():
    roles = {}

    for role_data in ROLES:
        role = Role.query.filter_by(name=role_data["name"]).first()

        if not role:
            role = Role(
                name=role_data["name"],
                description=role_data["description"],
            )
            db.session.add(role)

        roles[role_data["name"]] = role

    return roles


def seed_permissions():
    permissions = {}

    for permission_data in PERMISSIONS:
        permission = Permission.query.filter_by(
            name=permission_data["name"]
        ).first()

        if not permission:
            permission = Permission(
                name=permission_data["name"],
                description=permission_data["description"],
            )
            db.session.add(permission)

        permissions[permission_data["name"]] = permission

    return permissions


def seed_role_permissions(roles, permissions):
    for role_name, permission_names in ROLE_PERMISSIONS.items():
        role = roles[role_name]

        for permission_name in permission_names:
            permission = permissions[permission_name]

            if permission not in role.permissions:
                role.permissions.append(permission)


def main():
    app = create_app()

    with app.app_context():
        roles = seed_roles()
        permissions = seed_permissions()

        seed_role_permissions(roles, permissions)

        db.session.commit()

        print("RBAC seed completed successfully.")
        print(f"Roles: {Role.query.count()}")
        print(f"Permissions: {Permission.query.count()}")


if __name__ == "__main__":
    main()