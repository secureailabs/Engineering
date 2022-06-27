# -------------------------------------------------------------------------------
# Engineering
# emails.py
# -------------------------------------------------------------------------------
"""Models used by emails"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

from typing import List

from pydantic import EmailStr, Field, StrictStr

from models.common import SailBaseModel


class EmailRequest(SailBaseModel):
    to: List[EmailStr] = Field(...)
    subject: StrictStr = Field(...)
    body: StrictStr = Field(...)
