###################################################################################
# @author Prawal Gangwar
# @brief Models used by invites management service
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
###################################################################################

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import Field, StrictStr

from models.common import BasicObjectInfo, PyObjectId, SailBaseModel


class InviteType(Enum):
    DF_RESEARCHER = "DF_RESEARCHER"
    DF_SUBMITTER = "DF_SUBMITTER"
    USER = "USER"


class InviteState(Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class Invite_Base(SailBaseModel):
    email: str = Field(max_length=255)


class Invite_Db(Invite_Base):
    id: PyObjectId = Field(alias="_id")
    invite_created_time: datetime = Field(default_factory=datetime.utcnow)
    organization_id: PyObjectId = Field(...)
    state: InviteState = Field(...)


class RegisterInvite_In(Invite_Base):
    pass


class RegisterInvite_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")


class UpdateInvite_In(SailBaseModel):
    # todo: Prawal add a validator to enure that atleast of the field is present in the request
    description: Optional[StrictStr] = Field(default=None)
    name: Optional[StrictStr] = Field(default=None)
    keywords: Optional[StrictStr] = Field(default=None)
    version: Optional[StrictStr] = Field(default=None)


class GetInvite_Out(Invite_Base):
    invite_created_time: datetime = Field(...)
    organization: BasicObjectInfo = Field(...)
    state: InviteState = Field(...)


class GetMultipleInvite_Out(SailBaseModel):
    invites: List[GetInvite_Out] = Field(...)
