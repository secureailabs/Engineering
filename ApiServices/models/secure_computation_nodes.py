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
    STANDARD_B4MS = "STANDARD_B4MS"


class SecureComputationNodeState(Enum):
    REQUESTED = "REQUESTED"
    CREATING = "CREATING"
    INITIALIZING = "INITIALIZING"
    WAITING_FOR_DATA = "WAITING_FOR_DATA"
    FAILED = "FAILED"
    READY = "READY"
    DELETED = "DELETED"
    DELETING = "DELETING"
    DELETE_FAILED = "DELETE_FAILED"


class SecureComputationNode_Base(SailBaseModel):
    name: StrictStr = Field(...)
    digital_contract_id: PyObjectId = Field(...)
    dataset_id: PyObjectId = Field(...)
    type: SecureComputationNodeType = Field(...)


class SecureComputationNode_Db(SecureComputationNode_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    researcher_user_id: PyObjectId = Field(...)
    state: SecureComputationNodeState = Field(...)
    details: Optional[StrictStr] = Field(default=None)
    ipaddress: Optional[IPv4Address] = Field(default=None)
    researcher_id: PyObjectId = Field(default=None)
    data_owner_id: PyObjectId = Field(default=None)


class RegisterSecureComputationNode_In(SecureComputationNode_Base):
    pass


class RegisterSecureComputationNode_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")


class GetSecureComputationNode_Out(SecureComputationNode_Db):
    pass


class UpdateSecureComputationNode_In(SailBaseModel):
    state: SecureComputationNodeState = Field(default=None)
