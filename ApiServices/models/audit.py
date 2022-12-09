# -------------------------------------------------------------------------------
# Engineering
# audit.py
# -------------------------------------------------------------------------------
"""Models used by audit query service"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
from pydantic import Field, StrictStr

from models.common import SailBaseModel


class QueryResult(SailBaseModel):
    status: StrictStr = Field(...)
    data: dict = Field(...)


class QueryRequest(SailBaseModel):
    query: StrictStr = Field(...)
    limit: int = 100
