# -------------------------------------------------------------------------------
# Engineering
# dataset_versions.py
# -------------------------------------------------------------------------------
"""Models used by dataset versions"""
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


class DatasetVersionState(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    NOT_UPLOADED = "NOT_UPLOADED"
    ERROR = "ERROR"


class DatasetVersionTableCoumn(SailBaseModel):
    id: PyObjectId = Field(...)
    units: StrictStr = Field(...)
    name: StrictStr = Field(...)
    tags: StrictStr = Field(...)
    type: StrictStr = Field(...)
    description: StrictStr = Field(...)


class DatasetVersion_Base(SailBaseModel):
    dataset_id: PyObjectId = Field(...)
    description: StrictStr = Field(...)
    name: str = Field(max_length=255)
    keywords: StrictStr = Field(...)
    publish_date: int = Field(...)


class DatasetVersion_Db(DatasetVersion_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    dataset_version_created_time: datetime = Field(default_factory=datetime.utcnow)
    organization_id: PyObjectId = Field(...)
    state: DatasetVersionState = Field(...)
    note: StrictStr = Field(default="")


class RegisterDatasetVersion_In(DatasetVersion_Base):
    pass


class RegisterDatasetVersion_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")


class UpdateDatasetVersion_In(SailBaseModel):
    # TODO: add a validator to enure that atleast of the field is present in the request
    description: Optional[StrictStr] = Field(default=None)
    name: Optional[StrictStr] = Field(default=None)
    keywords: Optional[StrictStr] = Field(default=None)


class GetDatasetVersion_Out(DatasetVersion_Base):
    dataset_version_created_time: datetime = Field(...)
    organization: BasicObjectInfo = Field(...)
    state: DatasetVersionState = Field(...)
    note: StrictStr = Field(...)


class GetDatasetVersionConnectionString_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")
    connection_string: StrictStr = Field(...)


class GetMultipleDatasetVersion_Out(SailBaseModel):
    dataset_versions: List[GetDatasetVersion_Out] = Field(...)
