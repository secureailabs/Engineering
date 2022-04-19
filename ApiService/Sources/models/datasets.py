from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, StrictStr
from models.common import PyObjectId


class DatasetBase(BaseModel):
    Description: StrictStr = Field(...)
    Version: StrictStr = Field(...)
    Name: StrictStr = Field(...)
    Keywords: StrictStr = Field(...)
    PublishDate: datetime = Field(...)
    JurisdictionalLimitations: StrictStr = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class RegisterDataset_In(DatasetBase):
    pass


class RegisterDataset_Out(BaseModel):
    id: PyObjectId = Field(alias="_id")


class Dataset_Db(DatasetBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
