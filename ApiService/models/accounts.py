from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, StrictStr
from models.common import PyObjectId


class Organization_Base(BaseModel):
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


class Organization_db(Organization_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    accountCreatedTime: datetime = Field(default_factory=datetime.utcnow)


class RegisterOrganization_In(Organization_Base):
    pass


class RegisterOrganization_Out(BaseModel):
    id: PyObjectId = Field(...)


class GetOrganizations_Out(Organization_Base):
    id: PyObjectId = Field(...)


class UpdateOrganization_In(BaseModel):
    primaryContactName: Optional[StrictStr] = Field(...)
    primaryContactTitle: Optional[StrictStr] = Field(...)
    primaryContactEmail: Optional[EmailStr] = Field(...)
    primaryContactPhone: Optional[StrictStr] = Field(...)
    secondaryContactName: Optional[StrictStr] = Field(...)
    secondaryContactTitle: Optional[StrictStr] = Field(...)
    secondaryContactEmail: Optional[EmailStr] = Field(...)
    secondaryContactPhone: Optional[StrictStr] = Field(...)


class UserRole(Enum):
    Admin = "Admin"
    Auditor = "Auditor"
    User = "User"
    DigitalContractAdmin = "DigitalContractAdmin"
    DatasetAdmin = "DatasetAdmin"
    SailAdmin = "SailAdmin"


class UserAccountState(Enum):
    Active = "Active"
    Inactive = "Inactive"
    Locked = "Locked"


class User_Base(BaseModel):
    username: StrictStr = Field(...)
    email: EmailStr = Field(...)
    title: StrictStr = Field(...)
    phone: StrictStr = Field(...)
    role: UserRole = Field(...)


class User_Db(User_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    accountCreationTime: datetime = Field(default_factory=datetime.utcnow)
    hashed_password: StrictStr = Field(...)
    accountState: UserAccountState = Field(...)


class RegisterUser_In(User_Base):
    password: str = Field(...)


class RegisterUser_Out(User_Base):
    id: PyObjectId = Field(...)


class GetUsers_Out(User_Base):
    id: PyObjectId = Field(...)


class UpdateUser_In(BaseModel):
    title: Optional[StrictStr] = Field(None)
    phone: Optional[StrictStr] = Field(...)
    role: Optional[UserRole] = Field(...)
    accountState: Optional[UserAccountState] = Field(...)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
