###################################################################################
# @author Prawal Gangwar
# @brief Models used by account management service
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
###################################################################################

from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import Field, StrictStr
from models.common import PyObjectId, SailBaseModel


class DatasetFamilyState(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class DatasetFamily_Base(SailBaseModel):
    # TODO: Prawal add a StrictStr validator for string lenght
    title: StrictStr = Field(...)
    description: StrictStr = Field(...)
    tag: StrictStr = Field(...)
    version: StrictStr = Field(...)


class DatasetFamily_Db(DatasetFamily_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    creation_time: datetime = Field(default_factory=datetime.utcnow)
    organization_id: PyObjectId = Field(...)
    state: DatasetFamilyState = Field(...)


class RegisterDatasetFamily_In(DatasetFamily_Base):
    pass


class RegisterDatasetFamily_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")


class UpdateDatasetFamily_In(SailBaseModel):
    # todo: Prawal add a validator to enure that atleast of the field is present in the request
    title: Optional[StrictStr] = Field(default=None)
    description: Optional[StrictStr] = Field(default=None)
    tag: Optional[StrictStr] = Field(default=None)
    version: Optional[StrictStr] = Field(default=None)


class GetDatasetFamily_Out(DatasetFamily_Db):
    pass
