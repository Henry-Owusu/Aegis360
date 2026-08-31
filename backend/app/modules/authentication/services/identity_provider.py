from dataclasses import dataclass
import uuid


@dataclass
class Identity:
    object_id: str
    email: str
    first_name: str
    last_name: str


class MockIdentityProvider:

    @staticmethod
    def authenticate(email: str) -> Identity:
        users = {
            "dpo@aegis360.com": Identity(
                object_id=str(uuid.uuid5(uuid.NAMESPACE_DNS, "dpo@aegis360.com")),
                email="dpo@aegis360.com",
                first_name="Demo",
                last_name="DPO",
            ),
            "dps@aegis360.com": Identity(
                object_id=str(uuid.uuid5(uuid.NAMESPACE_DNS, "dps@aegis360.com")),
                email="dps@aegis360.com",
                first_name="Demo",
                last_name="DPS",
            ),
            "pm@aegis360.com": Identity(
                object_id=str(uuid.uuid5(uuid.NAMESPACE_DNS, "pm@aegis360.com")),
                email="pm@aegis360.com",
                first_name="Demo",
                last_name="PM",
            ),
            "auditor@aegis360.com": Identity(
                object_id=str(uuid.uuid5(uuid.NAMESPACE_DNS, "auditor@aegis360.com")),
                email="auditor@aegis360.com",
                first_name="Demo",
                last_name="Auditor",
            ),
            "approver@aegis360.com": Identity(
                object_id=str(uuid.uuid5(uuid.NAMESPACE_DNS, "approver@aegis360.com")),
                email="approver@aegis360.com",
                first_name="Demo",
                last_name="Approver",
            ),
            "admin@aegis360.com": Identity(
                object_id=str(uuid.uuid5(uuid.NAMESPACE_DNS, "admin@aegis360.com")),
                email="admin@aegis360.com",
                first_name="Demo",
                last_name="Administrator",
            ),
        }

        identity = users.get(email.lower())

        if not identity:
            raise ValueError("Unknown mock user")

        return identity