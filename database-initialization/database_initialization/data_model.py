# -------------------------------------------------------------------------------
# database_initialization
# data_model.py
# -------------------------------------------------------------------------------
"""Organization manager class to manage organizations"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

import json
from typing import List, Optional

from pydantic import BaseModel
from sail_client import AuthenticatedClient
from sail_client.api.default import (
    commit_data_model_version,
    register_data_model,
    register_data_model_version,
    save_data_model,
    update_data_model,
)
from sail_client.models import (
    CommitDataModelVersionIn,
    RegisterDataModelIn,
    RegisterDataModelOut,
    RegisterDataModelVersionIn,
    RegisterDataModelVersionOut,
    SaveDataModelVersionIn,
    UpdateDataModelIn,
)


class SeriesDataModelType(str):
    SeriesDataModelCategorical = "SeriesDataModelCategorical"
    SeriesDataModelDate = "SeriesDataModelDate"
    SeriesDataModelDateTime = "SeriesDataModelDateTime"
    SeriesDataModelInterval = "SeriesDataModelInterval"
    SeriesDataModelUnique = "SeriesDataModelUnique"


class DataModelSeriesSchema(BaseModel):
    type: SeriesDataModelType
    list_value: Optional[List[str]]
    unit: Optional[str]
    min: Optional[float]
    max: Optional[float]
    resolution: Optional[float]


class DataModelSeriesLocal(BaseModel):
    id: str
    name: str
    description: str
    series_schema: DataModelSeriesSchema


class DataModelDataframeLocal(BaseModel):
    id: str
    name: str
    description: str
    series: List[DataModelSeriesLocal]


class DataModel(BaseModel):
    name: str
    description: str
    dataframes: List[DataModelDataframeLocal]


class DataModelManager:
    def __init__(self, data_model_json: str, authenticated_client: AuthenticatedClient):
        self.authenticated_client = authenticated_client
        # Load data model from file
        self.data_model = DataModel.parse_obj(json.loads(data_model_json))

    def register_data_model(self):
        print("Registering data model")
        # Register data model
        data_model = RegisterDataModelIn(name=self.data_model.name, description=self.data_model.name)
        data_model_resp = register_data_model.sync(client=self.authenticated_client, json_body=data_model)
        assert type(data_model_resp) == RegisterDataModelOut

        # Register data model version
        data_model_version = RegisterDataModelVersionIn(
            name=self.data_model.name, description=self.data_model.description, data_model_id=data_model_resp.id
        )
        data_model_version_resp = register_data_model_version.sync(
            client=self.authenticated_client, json_body=data_model_version
        )
        assert type(data_model_version_resp) == RegisterDataModelVersionOut

        data_model_dict = {"dataframes": [dataframe.dict() for dataframe in self.data_model.dataframes]}
        save_req = SaveDataModelVersionIn.from_dict(data_model_dict)
        # Save data model version
        save_data_model.sync(
            client=self.authenticated_client, data_model_version_id=data_model_version_resp.id, json_body=save_req
        )

        # Commit the data model version
        commit_req = CommitDataModelVersionIn(commit_message="Initial commit")
        commit_data_model_version.sync(
            client=self.authenticated_client, data_model_version_id=data_model_version_resp.id, json_body=commit_req
        )

        return data_model_resp.id
