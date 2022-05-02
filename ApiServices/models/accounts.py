###################################################################################
# @author Prawal Gangwar
# @brief Models used by account management service
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
###################################################################################

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import Field, EmailStr, StrictStr
from models.common import PyObjectId, SailBaseModel


class OrganizationState(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Organization_Base(SailBaseModel):
    name: StrictStr = Field(...)
    description: StrictStr = Field(...)
    avatar: Optional[StrictStr] = Field(default=None)


class Organization_db(Organization_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    accountCreatedTime: datetime = Field(default_factory=datetime.utcnow)
    organizationState: OrganizationState = Field(...)


class RegisterOrganization_In(Organization_Base):
    adminName: StrictStr = Field(...)
    adminJobTitle: StrictStr = Field(...)
    adminEmail: EmailStr = Field(...)
    adminPassword: StrictStr = Field(...)
    adminAvatar: Optional[StrictStr] = Field(default=None)


class RegisterOrganization_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")


class GetOrganizations_Out(Organization_Base):
    id: PyObjectId = Field(alias="_id")


class UpdateOrganization_In(SailBaseModel):
    # TODO: Prawal add a validator to enure that atleast of the field is present in the request
    name: Optional[StrictStr] = Field(...)
    description: Optional[StrictStr] = Field(...)
    avatar: Optional[StrictStr] = Field(...)


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


class User_Base(SailBaseModel):
    username: StrictStr = Field(...)
    email: EmailStr = Field(...)
    jobTitle: StrictStr = Field(...)
    role: UserRole = Field(...)
    avatar: Optional[StrictStr] = Field(...)


class User_Db(User_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    accountCreationTime: datetime = Field(default_factory=datetime.utcnow)
    hashedPassword: StrictStr = Field(...)
    accountState: UserAccountState = Field(...)
    organizationId: PyObjectId = Field(...)


class UserInfo_Out(User_Base):
    id: PyObjectId = Field(alias="_id")
    organizationId: PyObjectId = Field(...)


class RegisterUser_In(User_Base):
    password: str = Field(...)


class RegisterUser_Out(User_Base):
    id: PyObjectId = Field(alias="_id")


class GetUsers_Out(User_Base):
    id: PyObjectId = Field(alias="_id")


class UpdateUser_In(SailBaseModel):
    jobTitle: Optional[StrictStr] = Field(...)
    role: Optional[UserRole] = Field(...)
    accountState: Optional[UserAccountState] = Field(...)
    avatar: Optional[StrictStr] = Field(...)
