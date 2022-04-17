from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, StrictStr
from models.users import PyObjectId


class OrganizationBase(BaseModel):
    name: StrictStr = Field(...)
    address: StrictStr = Field(...)
    primaryContactName: StrictStr = Field(...)
    primaryContactTitle: StrictStr = Field(...)
    primaryContactEmail: EmailStr = Field(...)
    primaryContactPhone: StrictStr = Field(...)
    secondaryContactName: StrictStr = Field(...)
    secondaryContactTitle: StrictStr = Field(...)
    secondaryContactEmail: EmailStr = Field(...)
    secondaryContactPhone: StrictStr = Field(...)

    class Config:
        allow_mutation = False
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class RegisterOrganization_In(OrganizationBase):
    pass


class RegisterOrganization_Out(OrganizationBase):
    accountCreatedTime: datetime = Field(...)


class Organization_db(OrganizationBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    accountCreatedTime: datetime = Field(default_factory=datetime.utcnow)
