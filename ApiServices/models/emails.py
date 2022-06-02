###################################################################################
# @author Prawal Gangwar
# @brief Models used by email service
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
###################################################################################

from pydantic import EmailStr, Field, SecretStr, StrictStr

from models.common import SailBaseModel


class SenderCredentials(SailBaseModel):
    email: EmailStr = Field(...)
    password: SecretStr = Field(...)


class EmailRequest(SailBaseModel):
    to: EmailStr = Field(...)
    subject: StrictStr = Field(...)
    body: StrictStr = Field(...)
