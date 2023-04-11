from enum import Enum


class DataFederationProvisionState(str, Enum):
    CREATING = "CREATING"
    CREATED = "CREATED"
    CREATION_FAILED = "CREATION_FAILED"
    DELETING = "DELETING"
    DELETED = "DELETED"
    DELETION_FAILED = "DELETION_FAILED"

    def __str__(self) -> str:
        return str(self.value)
