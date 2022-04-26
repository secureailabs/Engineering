from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, StrictStr
from models.common import PyObjectId
from enum import Enum


class DigitalContractState(Enum):
    New = "New"
    Accepted = "Accepted"
    Activated = "Activated"
    Rejected = "Rejected"
    Archived = "Archived"


class DigitalContractBase(BaseModel):

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class RegisterDigitalContract_In(DigitalContractBase):
    Title: StrictStr = Field(...)
    Description: StrictStr = Field(...)
    Version: StrictStr = Field(...)
    DatasetIdentifier: PyObjectId = Field(...)
    SubscriptionDays: int = Field(...)
    LegalAgreement: StrictStr = Field(...)


class RegisterDigitalContract_Out(DigitalContractBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")


class DigitalContract_Db(RegisterDigitalContract_In):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    DataOwnerIdenfier: PyObjectId = Field(...)
    ResearcherIdentifier: PyObjectId = Field(...)
    Timestamp: datetime = Field(default_factory=datetime.utcnow)
    State: DigitalContractState = Field(...)
