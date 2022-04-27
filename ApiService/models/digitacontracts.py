from datetime import datetime
from pydantic import BaseModel, Field, StrictStr
from models.common import PyObjectId
from enum import Enum


class DigitalContractState(Enum):
    New = "New"
    Accepted = "Accepted"
    Activated = "Activated"
    Rejected = "Rejected"
    Archived = "Archived"


class RegisterDigitalContract_In(BaseModel):
    Title: StrictStr = Field(...)
    Description: StrictStr = Field(...)
    Version: StrictStr = Field(...)
    DatasetIdentifier: PyObjectId = Field(...)
    SubscriptionDays: int = Field(...)
    LegalAgreement: StrictStr = Field(...)
    Region: StrictStr = Field(...)


class AcceptDigitalContract_In(BaseModel):
    RetentionTime: int = Field(...)
    LegalAgreement: StrictStr = Field(...)
    Region: StrictStr = Field(...)


class DigitalContract_Db(RegisterDigitalContract_In, AcceptDigitalContract_In):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    DataOwnerIdenfier: PyObjectId = Field(...)
    ResearcherIdentifier: PyObjectId = Field(...)
    Timestamp: datetime = Field(default_factory=datetime.utcnow)
    State: DigitalContractState = Field(...)


class RegisterDigitalContract_Out(BaseModel):
    id: PyObjectId = Field(...)


class GetDigitalContract_Out(DigitalContract_Db):
    pass
