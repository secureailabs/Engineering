from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, StrictStr
from models.common import PyObjectId


class DatasetFamily_Base(BaseModel):
    DatasetFamilyDescription: StrictStr = Field(...)
    DatasetFamilyTags: StrictStr = Field(...)
    DatasetFamilyTitle: StrictStr = Field(...)


class DatasetFamily_Db(DatasetFamily_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    creationTime: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class RegisterDatasetFamily_In(DatasetFamily_Base):
    pass


class RegisterDatasetFamily_Out(DatasetFamily_Base):
    id: PyObjectId = Field(...)


class GetDatasetFamily_Out(DatasetFamily_Base):
    pass


class UpdateDatasetFamily_In(BaseModel):
    pass
