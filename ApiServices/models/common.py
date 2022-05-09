###################################################################################
# @author Prawal Gangwar
# @brief Common utilities for the API Services
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
###################################################################################

from uuid import UUID, uuid4
from pydantic import BaseModel


class PyObjectId(UUID):
    def __init__(self):
        return super().__init__(str(uuid4()))

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        uuid_obj = UUID(str(v), version=4)
        return UUID(str(v), version=4)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class SailBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
