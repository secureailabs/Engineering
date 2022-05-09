###################################################################################
# @author Prawal Gangwar
# @brief Models used by secure computation nodes apis
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
###################################################################################

from datetime import datetime
from enum import Enum
from ipaddress import IPv4Address
from typing import Optional
from pydantic import Field, StrictStr
from models.common import PyObjectId, SailBaseModel


class SecureComputationNodeType(Enum):
    Standard_B4ms = "Standard_B4ms"


class SecureComputationNodeState(Enum):
    Requested = "Requested"
    Creating = "Creating"
    Initializing = "Initializing"
    Ready = "Ready"
    Deleted = "Deleted"
    Deleting = "Deleting"
    Failed = "Failed"


class SecureComputationNode_Base(SailBaseModel):
    name: StrictStr = Field(...)
    digitalContractId: PyObjectId = Field(...)
    datasetId: PyObjectId = Field(...)
    type: SecureComputationNodeType = Field(...)


class SecureComputationNode_Db(SecureComputationNode_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    researcherUserId: PyObjectId = Field(...)
    state: SecureComputationNodeState = Field(...)
    details: Optional[StrictStr] = Field(default=None)
    ipaddress: Optional[IPv4Address] = Field(default=None)
    researcherId: PyObjectId = Field(default=None)
    dataOwnerId: PyObjectId = Field(default=None)


class RegisterSecureComputationNode_In(SecureComputationNode_Base):
    pass


class RegisterSecureComputationNode_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")


class GetSecureComputationNode_Out(SecureComputationNode_Db):
    pass


class UpdateSecureComputationNode_In(SailBaseModel):
    state: SecureComputationNodeState = Field(default=None)
