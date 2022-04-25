from typing import List
from bson import ObjectId
from pydantic import BaseModel, Field, StrictStr


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Eosb(BaseModel):
    OrganizationGuid: StrictStr = Field(...)
    AccessRights: int = Field(...)
    Eosb: StrictStr = Field(...)
    UserGuid: StrictStr = Field(...)
    Status: int = Field(...)


class DatasetBase(BaseModel):
    Description: StrictStr = Field(...)
    Version: StrictStr = Field(...)
    Name: StrictStr = Field(...)
    Keywords: StrictStr = Field(...)
    PublishDate: int = Field(...)
    JurisdictionalLimitations: StrictStr = Field(...)


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
    Eosb: Eosb
    DatasetGuid: StrictStr = Field(...)
    DatasetData: DatasetModel = Field(...)


class RegisterDataset_Out(BaseModel):
    pass


class GetDatasets_In(BaseModel):
    Eosb: Eosb
    pass


class GetDatasets_Out(BaseModel):
    pass


class GetDataset_In(BaseModel):
    Eosb: Eosb
    DatasetGuid: StrictStr = Field(...)
    pass


class GetDataset_Out(BaseModel):
    pass


class DeleteDataset_In(BaseModel):
    Eosb: Eosb
    pass


class DeleteDataset_Out(BaseModel):
    pass
