from enum import Enum


class DataModelState(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    DELETED = "DELETED"

    def __str__(self) -> str:
        return str(self.value)
