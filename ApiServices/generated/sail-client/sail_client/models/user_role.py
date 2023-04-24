from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    AUDITOR = "AUDITOR"
    USER = "USER"
    DIGITAL_CONTRACT_ADMIN = "DIGITAL_CONTRACT_ADMIN"
    DATASET_ADMIN = "DATASET_ADMIN"
    SAIL_ADMIN = "SAIL_ADMIN"
    ORGANIZATION_ADMIN = "ORGANIZATION_ADMIN"

    def __str__(self) -> str:
        return str(self.value)
