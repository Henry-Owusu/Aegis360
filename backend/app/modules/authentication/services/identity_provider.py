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
            "dpo@aegis360.local": Identity(
                object_id=str(uuid.uuid5(uuid.NAMESPACE_DNS, "dpo@aegis360.local")),
                email="dpo@aegis360.local",
                first_name="Demo",
                last_name="DPO",
            ),
            "dps@aegis360.local": Identity(
                object_id=str(uuid.uuid5(uuid.NAMESPACE_DNS, "dps@aegis360.local")),
                email="dps@aegis360.local",
                first_name="Demo",
                last_name="DPS",
            ),
            "pm@aegis360.local": Identity(
                object_id=str(uuid.uuid5(uuid.NAMESPACE_DNS, "pm@aegis360.local")),
                email="pm@aegis360.local",
                first_name="Demo",
                last_name="PM",
            ),
            "auditor@aegis360.local": Identity(
                object_id=str(uuid.uuid5(uuid.NAMESPACE_DNS, "auditor@aegis360.local")),
                email="auditor@aegis360.local",
                first_name="Demo",
                last_name="Auditor",
            ),
            "approver@aegis360.local": Identity(
                object_id=str(uuid.uuid5(uuid.NAMESPACE_DNS, "approver@aegis360.local")),
                email="approver@aegis360.local",
                first_name="Demo",
                last_name="Approver",
            ),
            "admin@aegis360.local": Identity(
                object_id=str(uuid.uuid5(uuid.NAMESPACE_DNS, "admin@aegis360.local")),
                email="admin@aegis360.local",
                first_name="Demo",
                last_name="Administrator",
            ),
        }

        identity = users.get(email.lower())

        if not identity:
            raise ValueError("Unknown mock user")

        return identity