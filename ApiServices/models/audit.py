# -------------------------------------------------------------------------------
# Engineering
# audit.py
# -------------------------------------------------------------------------------
"""Models used by audit query service"""
import time
from typing import Optional, Union

from models.common import SailBaseModel
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
from pydantic import Field, StrictStr


class QueryResult(SailBaseModel):
    status: StrictStr = Field(...)
    data: dict = Field(...)
