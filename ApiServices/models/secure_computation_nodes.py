# -------------------------------------------------------------------------------
# Engineering
# secure_computation_nodes.py
# -------------------------------------------------------------------------------
"""Models used by secure computation nodes apis"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

from datetime import datetime
from enum import Enum
from ipaddress import IPv4Address
from typing import List, Optional

from pydantic import Field, StrictStr

from models.common import BasicObjectInfo, PyObjectId, SailBaseModel


class SecureComputationNodeType(Enum):
    Standard_D4s_v4 = "Standard_D4s_v4"


class SecureComputationNodeState(Enum):
    REQUESTED = "REQUESTED"
    CREATING = "CREATING"
    INITIALIZING = "INITIALIZING"
    WAITING_FOR_DATA = "WAITING_FOR_DATA"
    FAILED = "FAILED"
    READY = "READY"
    IN_USE = "IN_USE"
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
    detail: Optional[StrictStr] = Field(default=None)
    ipaddress: Optional[IPv4Address] = Field(default=None)
    researcher_id: PyObjectId = Field(default=None)
    data_owner_id: PyObjectId = Field(default=None)


class RegisterSecureComputationNode_In(SecureComputationNode_Base):
    pass


class RegisterSecureComputationNode_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")


class GetSecureComputationNode_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")
    name: StrictStr = Field(...)
    digital_contract: BasicObjectInfo = Field(...)
    dataset: BasicObjectInfo = Field(...)
    researcher: BasicObjectInfo = Field(default=None)
    data_owner: BasicObjectInfo = Field(default=None)
    researcher_user: BasicObjectInfo = Field(...)
    type: SecureComputationNodeType = Field(...)
    timestamp: datetime = Field(...)
    state: SecureComputationNodeState = Field(...)
    detail: Optional[StrictStr] = Field(default=None)
    ipaddress: Optional[IPv4Address] = Field(default=None)


class GetMultipleSecureComputationNode_Out(SailBaseModel):
    secure_computation_nodes: List[GetSecureComputationNode_Out] = Field(...)


class UpdateSecureComputationNode_In(SailBaseModel):
    state: SecureComputationNodeState = Field(default=None)
