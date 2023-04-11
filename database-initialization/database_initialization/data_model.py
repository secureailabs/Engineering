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
from typing import List

from pydantic import BaseModel
from sail_client import SyncAuthenticatedOperations
from sail_client.models import (
    RegisterDataModelDataframeIn,
    RegisterDataModelIn,
    RegisterDataModelSeriesIn,
    RegisterDataModelSeriesInSeriesSchema,
    UpdateDataModelDataframeIn,
    UpdateDataModelIn,
)


class SeriesDataModel(BaseModel):
    type: str
    series_name: str
    series_data_model_id: str


class DataFrameDataModel(BaseModel):
    type: str
    data_frame_name: str
    data_frame_data_model_id: str
    list_series_data_model: List[SeriesDataModel]


class DataModel(BaseModel):
    type: str
    tabular_dataset_data_model_id: str
    list_data_frame_data_model: List[DataFrameDataModel]


class DataModelManager:
    def __init__(self, data_model_json: str, sync_authenticated_operations: SyncAuthenticatedOperations):
        self.operations = sync_authenticated_operations

        # Load data model from file
        self.data_model = DataModel.parse_obj(json.loads(data_model_json))

        print(self.data_model.type)

    def register_data_model(self):
        # Register data model
        data_model = RegisterDataModelIn(name=self.data_model.type, description=self.data_model.type)
        data_model_resp = self.operations.register_data_model(json_body=data_model)

        # Register tabular dataset data model
        list_data_frame_ids = []
        for data_frame_data_model in self.data_model.list_data_frame_data_model:
            data_frame_data_model_req = RegisterDataModelDataframeIn(
                name=data_frame_data_model.data_frame_name,
                description=data_frame_data_model.data_frame_name,
            )
            dataframe_register_resp = self.operations.register_data_model_dataframe(json_body=data_frame_data_model_req)
            list_data_frame_ids.append(dataframe_register_resp.id)

            # Register series data model
            list_of_series_ids = []

            for series_data_model in data_frame_data_model.list_series_data_model:
                foo = RegisterDataModelSeriesInSeriesSchema()
                series_data_model = RegisterDataModelSeriesIn(
                    name=series_data_model.series_name,
                    description=series_data_model.series_name,
                    series_schema=foo,
                )
                register_series_resp = self.operations.register_data_model_series(json_body=series_data_model)
                list_of_series_ids.append(register_series_resp.id)

            # Update the data model dataframe with the list of series ids
            update_data_frame_req = UpdateDataModelDataframeIn(data_model_series_to_add=list_of_series_ids)
            self.operations.update_data_model_dataframe(
                data_model_dataframe_id=dataframe_register_resp.id, json_body=update_data_frame_req
            )
        # Update the data model with the list of data frame ids
        data_model_update_req = UpdateDataModelIn(data_model_dataframe_to_add=list_data_frame_ids)
        self.operations.update_data_model(data_model_id=data_model_resp.id, json_body=data_model_update_req)

        return data_model_resp.id
