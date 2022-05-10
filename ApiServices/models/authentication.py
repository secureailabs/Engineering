###################################################################################
# @author Prawal Gangwar
# @brief Models used by authentication services
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
###################################################################################

from pydantic import Field, StrictStr
from models.common import PyObjectId, SailBaseModel
from models.accounts import UserRole


class LoginSuccess_Out(SailBaseModel):
    access_token: StrictStr
    refresh_token: StrictStr
    token_type: StrictStr


class TokenData(SailBaseModel):
    id: PyObjectId = Field(alias="_id")
    organization_id: PyObjectId = Field(...)
    role: UserRole = Field(...)
    exp: int = Field(...)


class RefreshTokenData(SailBaseModel):
    id: PyObjectId = Field(alias="_id")
    organization_id: PyObjectId = Field(...)
    role: UserRole = Field(...)
    exp: int = Field(...)


class RefreshToken_In(SailBaseModel):
    refresh_token: StrictStr = Field(...)
