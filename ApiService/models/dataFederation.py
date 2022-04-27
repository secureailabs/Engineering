from bson import ObjectId
from pydantic import BaseModel, Field, StrictStr
from models.common import PyObjectId


class DatasetModel(BaseModel):
    JurisdictionalLimitations: StrictStr = Field(...)
    Description: StrictStr = Field(...)
    DatasetName: StrictStr = Field(...)
    Keywords: StrictStr = Field(...)
    VersionNumber: StrictStr = Field(...)
    PublishDate: int = Field(...)
    PrivacyLevel: int = Field(...)


class DataFederation_Db(DatasetModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    DatasetGuid: StrictStr = Field(...)
    DataOwnerGuid: StrictStr = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class RegisterDataFederation_In(BaseModel):
    pass


class RegisterDataFederation_Out(BaseModel):
    pass


class RegisterDataset_Out(BaseModel):
    pass


class GetDatasets_In(BaseModel):
    pass


class GetDatasets_Out(DatasetModel):
    pass


class GetDataset_In(BaseModel):
    pass


class GetDataset_Out(DatasetModel):
    DatasetGuid: StrictStr = Field(...)
    pass


class DeleteDataset_In(BaseModel):
    pass


class DeleteDataset_Out(BaseModel):
    pass
