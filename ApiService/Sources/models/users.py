from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr


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


class UserBase(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    phone: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class User_In(UserBase):
    pass


class User_Out(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    accountCreatedTime: datetime = Field(default_factory=datetime.utcnow)


class User_Db(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    accountCreatedTime: datetime = Field(default_factory=datetime.utcnow)
    passwordHash: str = Field(...)


class ScnModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    course: str = Field(...)
    gpa: float = Field(..., le=4.0)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": "3.0",
            }
        }


class AuthToken(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    userId: str
