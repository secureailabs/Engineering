from enum import Enum


class SecureComputationNodeSize(str, Enum):
    STANDARD_D4S_V4 = "Standard_D4s_v4"
    STANDARD_DC4ADS_V5 = "Standard_DC4ads_v5"

    def __str__(self) -> str:
        return str(self.value)
