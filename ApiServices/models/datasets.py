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


class DatasetState(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class DatasetTable(SailBaseModel):
    description: StrictStr = Field(...)
    tableIdentifier: StrictStr = Field(...)
    hashtags: StrictStr = Field(...)
    numberOfColumns: int = Field(...)
    name: StrictStr = Field(...)
    numberOfRows: int = Field(...)
    columnName: StrictStr = Field(...)


class Dataset_Base(SailBaseModel):
    id: PyObjectId = Field(alias="_id")
    description: StrictStr = Field(...)
    name: str = Field(max_length=255)
    keywords: StrictStr = Field(...)
    version: StrictStr = Field(...)
    publishDate: int = Field(...)
    tables: List[DatasetTable] = Field(...)


class Dataset_Db(Dataset_Base):
    datasetCreatedTime: datetime = Field(default_factory=datetime.utcnow)
    organizationId: PyObjectId = Field(...)
    state: DatasetState = Field(...)


class RegisterDataset_In(Dataset_Base):
    pass


class RegisterDataset_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")


class UpdateDataset_In(SailBaseModel):
    # TODO: Prawal add a validator to enure that atleast of the field is present in the request
    description: Optional[StrictStr] = Field(default=None)
    name: Optional[StrictStr] = Field(default=None)
    keywords: Optional[StrictStr] = Field(default=None)
    version: Optional[StrictStr] = Field(default=None)


class GetDataset_Out(Dataset_Db):
    pass
