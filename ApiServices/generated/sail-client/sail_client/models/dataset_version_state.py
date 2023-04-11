from enum import Enum


class DatasetVersionState(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    CREATING_DIRECTORY = "CREATING_DIRECTORY"
    NOT_UPLOADED = "NOT_UPLOADED"
    ENCRYPTING = "ENCRYPTING"
    ERROR = "ERROR"

    def __str__(self) -> str:
        return str(self.value)
