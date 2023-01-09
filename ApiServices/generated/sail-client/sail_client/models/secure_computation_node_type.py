from enum import Enum


class SecureComputationNodeType(str, Enum):
    SCN = "SCN"
    SMART_BROKER = "SMART_BROKER"

    def __str__(self) -> str:
        return str(self.value)
