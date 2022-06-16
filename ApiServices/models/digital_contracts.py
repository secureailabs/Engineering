# -------------------------------------------------------------------------------
# Engineering
# digital_contracts.py
# -------------------------------------------------------------------------------
"""Models used by digital_contracts"""
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
from typing import List, Optional

from pydantic import Field, StrictStr

from models.common import BasicObjectInfo, PyObjectId, SailBaseModel


class DigitalContractState(Enum):
    NEW = "NEW"
    ACCEPTED = "ACCEPTED"
    ACTIVATED = "ACTIVATED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"


class DigitalContract_Base(SailBaseModel):
    name: StrictStr = Field(...)
    description: StrictStr = Field(...)
    subscription_days: int = Field(...)
    legal_agreement: StrictStr = Field(...)
    version: StrictStr = Field(...)


class DigitalContract_Db(DigitalContract_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    data_owner_id: PyObjectId = Field(...)
    researcher_id: PyObjectId = Field(...)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    state: DigitalContractState = Field(...)
    dataset_id: PyObjectId = Field(...)


class RegisterDigitalContract_In(DigitalContract_Base):
    dataset_id: PyObjectId = Field(...)


class RegisterDigitalContract_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")


class AcceptDigitalContract_In(SailBaseModel):
    retention_time: int = Field(...)
    legal_agreement: StrictStr = Field(...)
    region: StrictStr = Field(...)


class GetDigitalContract_Out(DigitalContract_Base):
    id: PyObjectId = Field(alias="_id")
    data_owner: BasicObjectInfo = Field(...)
    researcher: BasicObjectInfo = Field(...)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    state: DigitalContractState = Field(...)
    dataset: BasicObjectInfo = Field(...)


class GetMultipleDigitalContract_Out(SailBaseModel):
    digital_contracts: List[GetDigitalContract_Out] = Field(...)


class UpdateDigitalContract_In(SailBaseModel):
    # todo: Prawal add a validator to enure that atleast of the field is present in the request
    name: Optional[StrictStr] = Field(default=None)
    description: Optional[StrictStr] = Field(default=None)
    subscription_days: Optional[int] = Field(default=None)
    legal_agreement: Optional[StrictStr] = Field(default=None)
    version: Optional[StrictStr] = Field(default=None)
    state: Optional[DigitalContractState] = Field(default=None)
