from enum import Enum


class DataFederationDataFormat(str, Enum):
    CSV = "CSV"
    FHIR = "FHIR"

    def __str__(self) -> str:
        return str(self.value)
