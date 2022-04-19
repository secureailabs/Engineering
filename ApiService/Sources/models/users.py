from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from models.common import PyObjectId


class UserBase(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    phone: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class User_In(UserBase):
    password: str = Field(...)


class User_Out(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    accountCreatedTime: datetime = Field(default_factory=datetime.utcnow)


class User_Db(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    accountCreatedTime: datetime = Field(default_factory=datetime.utcnow)
    hashed_password: str = Field(...)
    disabled: bool = Field(default=False)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
