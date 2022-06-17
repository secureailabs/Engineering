# -------------------------------------------------------------------------------
# Engineering
# data_federations.py
# -------------------------------------------------------------------------------
"""Models used by data federations"""
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


class DataFederationState(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class DataFederation_Base(SailBaseModel):
    name: StrictStr = Field(...)
    description: StrictStr = Field(...)


class DataFederation_Db(DataFederation_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    creation_time: datetime = Field(default_factory=datetime.utcnow)
    organization_id: PyObjectId = Field(...)
    state: DataFederationState = Field(...)
    data_submitter_organizations_id: List[PyObjectId] = Field(default_factory=list)
    research_organizations_id: List[PyObjectId] = Field(default_factory=list)
    dataset_families_id: List[PyObjectId] = Field(default_factory=list)
    invites_id: List[PyObjectId] = Field(default_factory=list)


class RegisterDataFederation_In(DataFederation_Base):
    pass


class RegisterDataFederation_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")


class UpdateDataFederation_In(SailBaseModel):
    name: Optional[StrictStr] = Field(default=None)
    description: Optional[StrictStr] = Field(default=None)


class GetDataFederation_Out(DataFederation_Base):
    id: PyObjectId = Field(alias="_id")
    creation_time: datetime = Field(default_factory=datetime.utcnow)
    organization: BasicObjectInfo = Field(...)
    state: DataFederationState = Field(...)
    data_submitter_organizations: List[BasicObjectInfo] = Field(...)
    research_organizations: List[BasicObjectInfo] = Field(...)
    dataset_families: List[BasicObjectInfo] = Field(...)
    invites: List[PyObjectId] = Field(...)


class GetMultipleDataFederation_Out(SailBaseModel):
    data_federations: List[GetDataFederation_Out] = Field(default_factory=list)
