# -------------------------------------------------------------------------------
# Engineering
# datasets.py
# -------------------------------------------------------------------------------
"""Models used by datasets"""
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


class DatasetState(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ERROR = "ERROR"


class Dataset_Base(SailBaseModel):
    # TODO: Prawal add a StrictStr validator for string lenght
    name: StrictStr = Field(...)
    description: StrictStr = Field(...)
    tags: StrictStr = Field(...)
    version: StrictStr = Field(...)


class Dataset_Db(Dataset_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    creation_time: datetime = Field(default_factory=datetime.utcnow)
    organization_id: PyObjectId = Field(...)
    state: DatasetState = Field(...)
    note: StrictStr = Field(default="")
    encryption_key_id: Optional[PyObjectId] = Field(default=None)


class RegisterDataset_In(Dataset_Base):
    pass


class RegisterDataset_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")


class UpdateDataset_In(SailBaseModel):
    # todo: Prawal add a validator to enure that atleast of the field is present in the request
    name: Optional[StrictStr] = Field(default=None)
    description: Optional[StrictStr] = Field(default=None)
    tag: Optional[StrictStr] = Field(default=None)
    version: Optional[StrictStr] = Field(default=None)


class GetDataset_Out(Dataset_Base):
    id: PyObjectId = Field(alias="_id")
    creation_time: datetime = Field(default_factory=datetime.utcnow)
    organization: BasicObjectInfo = Field(...)
    state: DatasetState = Field(...)
    note: StrictStr = Field(...)


class GetMultipleDataset_Out(SailBaseModel):
    datasets: List[GetDataset_Out] = Field(default_factory=list)
