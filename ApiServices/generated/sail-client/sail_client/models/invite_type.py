from enum import Enum


class InviteType(str, Enum):
    DF_RESEARCHER = "DF_RESEARCHER"
    DF_SUBMITTER = "DF_SUBMITTER"

    def __str__(self) -> str:
        return str(self.value)
