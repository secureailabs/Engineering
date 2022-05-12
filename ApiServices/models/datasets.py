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


class DatasetTableCoumn(SailBaseModel):
    id: PyObjectId = Field(...)
    units: StrictStr = Field(...)
    name: StrictStr = Field(...)
    tags: StrictStr = Field(...)
    type: StrictStr = Field(...)
    description: StrictStr = Field(...)


class DatasetTable(SailBaseModel):
    id: PyObjectId = Field(...)
    number_of_rows: int = Field(...)
    name: StrictStr = Field(...)
    tags: StrictStr = Field(...)
    number_of_columns: int = Field(...)
    compressed_data_size_in_bytes: int = Field(...)
    description: StrictStr = Field(...)
    all_column_properties: List[DatasetTableCoumn] = Field(...)
    data_size_in_bytes: int = Field(...)


class Dataset_Base(SailBaseModel):
    id: PyObjectId = Field(alias="_id")
    description: StrictStr = Field(...)
    name: str = Field(max_length=255)
    keywords: StrictStr = Field(...)
    version: StrictStr = Field(...)
    publish_date: int = Field(...)
    tables: List[DatasetTable] = Field(...)


class Dataset_Db(Dataset_Base):
    dataset_created_time: datetime = Field(default_factory=datetime.utcnow)
    organization_id: PyObjectId = Field(...)
    state: DatasetState = Field(...)


class RegisterDataset_In(Dataset_Base):
    pass


class RegisterDataset_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")


class UpdateDataset_In(SailBaseModel):
    # todo: Prawal add a validator to enure that atleast of the field is present in the request
    description: Optional[StrictStr] = Field(default=None)
    name: Optional[StrictStr] = Field(default=None)
    keywords: Optional[StrictStr] = Field(default=None)
    version: Optional[StrictStr] = Field(default=None)


class GetDataset_Out(Dataset_Db):
    pass
