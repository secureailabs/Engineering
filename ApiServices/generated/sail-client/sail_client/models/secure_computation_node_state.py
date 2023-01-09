from enum import Enum


class SecureComputationNodeState(str, Enum):
    REQUESTED = "REQUESTED"
    CREATING = "CREATING"
    INITIALIZING = "INITIALIZING"
    WAITING_FOR_DATA = "WAITING_FOR_DATA"
    FAILED = "FAILED"
    READY = "READY"
    IN_USE = "IN_USE"
    DELETED = "DELETED"
    DELETING = "DELETING"
    DELETE_FAILED = "DELETE_FAILED"

    def __str__(self) -> str:
        return str(self.value)
