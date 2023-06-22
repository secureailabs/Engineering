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
from sail_client.api.default import register_data_model, register_data_model_dataframe, register_data_model_series
from sail_client.models import (
    RegisterDataModelDataframeIn,
    RegisterDataModelDataframeOut,
    RegisterDataModelIn,
    RegisterDataModelOut,
    RegisterDataModelSeriesIn,
    RegisterDataModelSeriesOut,
    SeriesDataModelSchema,
    SeriesDataModelType,
)


class SeriesDataModel(BaseModel):
    type: str
    series_name: str
    list_value: Optional[List[str]]
    unit: Optional[str] = None
    min: Optional[float] = None
    max: Optional[float] = None
    resolution: Optional[float] = None


class DataFrameDataModel(BaseModel):
    type: str
    data_frame_name: str
    list_series_data_model: List[SeriesDataModel]


class DataModel(BaseModel):
    type: str
    list_data_frame_data_model: List[DataFrameDataModel]


class DataModelManager:
    def __init__(self, data_model_json: str, authenticated_client: AuthenticatedClient):
        self.authenticated_client = authenticated_client
        # Load data model from file
        self.data_model = DataModel.parse_obj(json.loads(data_model_json))

        print(self.data_model.type)

    def register_data_model(self):
        # Register data model
        data_model = RegisterDataModelIn(name=self.data_model.type, description=self.data_model.type)
        data_model_resp = register_data_model.sync(client=self.authenticated_client, json_body=data_model)
        assert type(data_model_resp) == RegisterDataModelOut

        # Register tabular dataset data model
        list_data_frame_ids = []
        for data_frame_data_model in self.data_model.list_data_frame_data_model:
            data_frame_data_model_req = RegisterDataModelDataframeIn(
                name=data_frame_data_model.data_frame_name,
                description=data_frame_data_model.data_frame_name,
                data_model_id=data_model_resp.id,
            )
            dataframe_register_resp = register_data_model_dataframe.sync(
                client=self.authenticated_client, json_body=data_frame_data_model_req
            )
            assert type(dataframe_register_resp) == RegisterDataModelDataframeOut
            list_data_frame_ids.append(dataframe_register_resp.id)

            # Register series data model
            list_of_series_ids = []

            for series_data_model in data_frame_data_model.list_series_data_model:
                series_data_model = RegisterDataModelSeriesIn(
                    name=series_data_model.series_name,
                    description=series_data_model.series_name,
                    data_model_dataframe_id=dataframe_register_resp.id,
                    series_schema=SeriesDataModelSchema(
                        type=SeriesDataModelType(series_data_model.type),
                        series_name=series_data_model.series_name,
                        list_value=series_data_model.list_value,  # type: ignore
                        unit=series_data_model.unit,  # type: ignore
                        min_=series_data_model.min,  # type: ignore
                        max_=series_data_model.max,  # type: ignore
                        resolution=series_data_model.resolution,  # type: ignore
                    ),
                )
                register_series_resp = register_data_model_series.sync(
                    client=self.authenticated_client, json_body=series_data_model
                )
                assert type(register_series_resp) == RegisterDataModelSeriesOut
                list_of_series_ids.append(register_series_resp.id)

        return data_model_resp.id