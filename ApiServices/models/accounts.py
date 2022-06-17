# -------------------------------------------------------------------------------
# Engineering
# accounts.py
# -------------------------------------------------------------------------------
"""Models used by account management service"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import EmailStr, Field, StrictStr

from models.common import BasicObjectInfo, PyObjectId, SailBaseModel


class OrganizationState(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Organization_Base(SailBaseModel):
    name: StrictStr = Field(...)
    description: StrictStr = Field(...)
    avatar: Optional[StrictStr] = Field(default=None)


class Organization_db(Organization_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    account_created_time: datetime = Field(default_factory=datetime.utcnow)
    state: OrganizationState = Field(...)


class RegisterOrganization_In(Organization_Base):
    admin_name: StrictStr = Field(...)
    admin_job_title: StrictStr = Field(...)
    admin_email: EmailStr = Field(...)
    admin_password: StrictStr = Field(...)
    admin_avatar: Optional[StrictStr] = Field(default=None)


class RegisterOrganization_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")


class GetOrganizations_Out(Organization_Base):
    id: PyObjectId = Field(alias="_id")


class GetMultipleOrganizations_Out(SailBaseModel):
    organizations: List[GetOrganizations_Out] = Field(...)


class UpdateOrganization_In(SailBaseModel):
    # TODO: Prawal add a validator to enure that atleast of the field is present in the request
    name: Optional[StrictStr] = Field(...)
    description: Optional[StrictStr] = Field(...)
    avatar: Optional[StrictStr] = Field(...)


class UserRole(Enum):
    ADMIN = "ADMIN"
    AUDITOR = "AUDITOR"
    USER = "USER"
    DIGITAL_CONTRACT_ADMIN = "DIGITAL_CONTRACT_ADMIN"
    DATASET_ADMIN = "DATASET_ADMIN"
    SAIL_ADMIN = "SAIL_ADMIN"


class UserAccountState(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class User_Base(SailBaseModel):
    name: StrictStr = Field(...)
    email: EmailStr = Field(...)
    job_title: StrictStr = Field(...)
    role: UserRole = Field(...)
    avatar: Optional[StrictStr] = Field(default=None)


class User_Db(User_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    account_creation_time: datetime = Field(default_factory=datetime.utcnow)
    hashed_password: StrictStr = Field(...)
    account_state: UserAccountState = Field(...)
    organization_id: PyObjectId = Field(...)


class UserInfo_Out(User_Base):
    id: PyObjectId = Field(alias="_id")
    organization: BasicObjectInfo = Field(...)


class RegisterUser_In(User_Base):
    password: str = Field(...)


class RegisterUser_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")


class GetUsers_Out(User_Base):
    id: PyObjectId = Field(alias="_id")
    organization: BasicObjectInfo = Field(...)
    name: StrictStr = Field(...)
    email: EmailStr = Field(...)
    job_title: StrictStr = Field(...)
    role: UserRole = Field(...)
    avatar: Optional[StrictStr] = Field(...)


class GetMultipleUsers_Out(SailBaseModel):
    users: List[GetUsers_Out] = Field(...)


class UpdateUser_In(SailBaseModel):
    job_title: Optional[StrictStr] = Field(...)
    role: Optional[UserRole] = Field(...)
    account_state: Optional[UserAccountState] = Field(...)
    avatar: Optional[StrictStr] = Field(...)
