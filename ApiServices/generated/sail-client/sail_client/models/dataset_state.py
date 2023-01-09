from enum import Enum


class DatasetState(str, Enum):
    CREATING_STORAGE = "CREATING_STORAGE"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ERROR = "ERROR"

    def __str__(self) -> str:
        return str(self.value)
