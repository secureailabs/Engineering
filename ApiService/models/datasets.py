from typing import List
from bson import ObjectId
from pydantic import BaseModel, Field, StrictStr
from models.common import PyObjectId


class DatasetTable(BaseModel):
    Description: StrictStr = Field(...)
    TableIdentifier: StrictStr = Field(...)
    Hashtags: StrictStr = Field(...)
    NumberColumns: int = Field(...)
    Name: StrictStr = Field(...)
    NumberRows: int = Field(...)
    ColumnName: StrictStr = Field(...)


class DatasetModel(BaseModel):
    JurisdictionalLimitations: StrictStr = Field(...)
    Description: StrictStr = Field(...)
    DatasetName: StrictStr = Field(...)
    Keywords: StrictStr = Field(...)
    VersionNumber: StrictStr = Field(...)
    PublishDate: int = Field(...)
    PrivacyLevel: int = Field(...)
    Tables: List[DatasetTable] = Field(...)


class Dataset_Db(DatasetModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    DatasetGuid: StrictStr = Field(...)
    DataOwnerGuid: StrictStr = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class RegisterDataset_In(BaseModel):
    DatasetGuid: StrictStr = Field(...)
    DatasetData: DatasetModel = Field(...)


class RegisterDataset_Out(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")


class GetDataset_Out(DatasetModel):
    DatasetGuid: StrictStr = Field(...)
    pass


class DeleteDataset_In(BaseModel):
    pass


class DeleteDataset_Out(BaseModel):
    pass
