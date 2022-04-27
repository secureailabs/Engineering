from datetime import datetime
from enum import Enum
from ipaddress import IPv4Address
from bson import ObjectId
from pydantic import BaseModel, Field, StrictStr
from models.common import PyObjectId


class ScnState(Enum):
    New = "New"
    Provisioning = "Provisioning"
    Initializing = "Initializing"
    WaitingForData = "WaitingForData"
    Ready = "Ready"
    Failed = "Failed"
    Deleting = "Deleting"
    Deleted = "Deleted"
    Archived = "Archived"


class Scn_Base(BaseModel):
    DatasetIdentifier: PyObjectId = Field(...)
    DigitalContractIdentifier: PyObjectId = Field(...)
    ScnType: StrictStr = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ProvisionScn_In(Scn_Base):
    pass


class ProvisionScn_Out(BaseModel):
    id: PyObjectId = Field(...)
    State: ScnState = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ScnModel_Db(Scn_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    CreationTime: datetime = Field(default_factory=datetime.utcnow)
    ResearcherIdentifier: PyObjectId = Field(...)
    State: ScnState = Field(...)
    IPAddress: IPv4Address = Field(...)
