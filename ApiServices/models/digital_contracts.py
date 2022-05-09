###################################################################################
# @author Prawal Gangwar
# @brief Models used by account management service
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
###################################################################################

from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import Field, StrictStr
from models.common import PyObjectId, SailBaseModel


class DigitalContractState(Enum):
    New = "New"
    Accepted = "Accepted"
    Activated = "Activated"
    Rejected = "Rejected"
    Archived = "Archived"


class DigitalContract_Base(SailBaseModel):
    name: StrictStr = Field(...)
    description: StrictStr = Field(...)
    subscriptionDays: int = Field(...)
    legalAgreement: StrictStr = Field(...)
    version: StrictStr = Field(...)
    datasetId: PyObjectId = Field(...)


class DigitalContract_Db(DigitalContract_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    dataOwnerId: PyObjectId = Field(...)
    researcherId: PyObjectId = Field(...)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    state: DigitalContractState = Field(...)


class RegisterDigitalContract_In(DigitalContract_Base):
    pass


class RegisterDigitalContract_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")


class AcceptDigitalContract_In(SailBaseModel):
    RetentionTime: int = Field(...)
    LegalAgreement: StrictStr = Field(...)
    Region: StrictStr = Field(...)


class GetDigitalContract_Out(DigitalContract_Db):
    pass


class UpdateDigitalContract_In(SailBaseModel):
    # TODO: Prawal add a validator to enure that atleast of the field is present in the request
    name: Optional[StrictStr] = Field(default=None)
    description: Optional[StrictStr] = Field(default=None)
    subscriptionDays: Optional[int] = Field(default=None)
    legalAgreement: Optional[StrictStr] = Field(default=None)
    version: Optional[StrictStr] = Field(default=None)
    state: Optional[DigitalContractState] = Field(default=None)
