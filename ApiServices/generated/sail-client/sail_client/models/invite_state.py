from enum import Enum


class InviteState(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

    def __str__(self) -> str:
        return str(self.value)
