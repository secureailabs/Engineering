from enum import Enum


class DatasetFormat(str, Enum):
    FHIR = "FHIR"
    CSV = "CSV"

    def __str__(self) -> str:
        return str(self.value)
