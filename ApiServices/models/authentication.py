# -------------------------------------------------------------------------------
# Engineering
# authentication.py
# -------------------------------------------------------------------------------
"""Models used by authentication services"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

from enum import Enum
from typing import List

from pydantic import Field, StrictStr

from models.accounts import UserRole
from models.common import PyObjectId, SailBaseModel


class LoginSuccess_Out(SailBaseModel):
    access_token: StrictStr = Field()
    refresh_token: StrictStr = Field()
    token_type: StrictStr = Field()


class TokenScope(Enum):
    PARTICIPANT_SCN = "PARTICIPANT_SCN"
    AGGREGATOR_SCN = "AGGREGATOR_SCN"
    COMPUTE = "COMPUTE"
    DATASET = "DATASET"
    ACCOUNT = "ACCOUNT"


class TokenData(SailBaseModel):
    id: PyObjectId = Field()
    organization_id: PyObjectId = Field()
    role: UserRole = Field()
    exp: int = Field()
    scope: List[TokenScope] = Field()


class RefreshTokenData(SailBaseModel):
    id: PyObjectId = Field()
    organization_id: PyObjectId = Field()
    role: UserRole = Field()
    exp: int = Field()
    scope: List[TokenScope] = Field()


class RefreshToken_In(SailBaseModel):
    refresh_token: StrictStr = Field()
