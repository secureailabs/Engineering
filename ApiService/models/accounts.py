from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, StrictStr
from models.common import PyObjectId


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


from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from models.common import PyObjectId


class UserInfo(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    phone: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserBase(UserInfo):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")


class User_In(UserInfo):
    password: str = Field(...)


class User_Out(UserBase):
    accountCreatedTime: datetime = Field(default_factory=datetime.utcnow)


class User_Db(UserBase):
    accountCreatedTime: datetime = Field(default_factory=datetime.utcnow)
    hashed_password: str = Field(...)
    disabled: bool = Field(default=False)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
