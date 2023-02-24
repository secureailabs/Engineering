from typing import List

import requests


def read_longitudinal_fhirv1(session):
    result = requests.post(
        session.get_url() + "/ingestion/read_longitudinal/fhirv1",
        params=None,
        verify=False,
    )
    return result.json()["longitudinal_id"]


def parse_dataset_tabular_from_longitudinal(
    session,
    longitudinal_id,
    dataset_federation_id,
    dataset_federation_name,
    data_model_tabular_id,
):
    payload = {
        "longitudinal_id": longitudinal_id,
        "dataset_federation_id": dataset_federation_id,
        "dataset_federation_name": dataset_federation_name,
        "data_model_tabular_id": data_model_tabular_id,
    }
    result = requests.post(
        session.get_url() + "/ingestion/read_dataset_tabular_from_longitudinal",
        params=payload,
        verify=False,
    )
    return result.json()["dataset_id"]


def parse_dataset_tabular_from_fhirv1(session, dataset_federation_id, dataset_federation_name, data_model_tabular_id):

    payload = {
        "dataset_federation_id": dataset_federation_id,
        "dataset_federation_name": dataset_federation_name,
        "data_model_tabular_id": data_model_tabular_id,
    }

    result = requests.post(session.get_url() + "/ingestion/dataset_tabular/fhirv1", params=payload, verify=False)
    return result.json()["dataset_id"]


def data_frame_tabular_select_data_frame(session, data_frame_tabular_id, data_frame_name):
    payload = {
        "data_frame_tabular_id": data_frame_tabular_id,
        "data_frame_name": data_frame_name,
    }
    result = requests.post(
        session.get_url() + "/data_frame_tabular/select_dataframe/" + data_frame_tabular_id,
        params=payload,
        verify=False,
    )
    return result.json()["data_frame_id"]


def data_frame_select_series(session, data_frame_id, series_name):
    payload = {"data_frame_id": data_frame_id, "series_name": series_name}
    result = requests.post(
        session.get_url() + "/data_frame/select_series/" + data_frame_id,
        params=payload,
        verify=False,
    )
    return result.json()["series_id"]


def read_dataset_csvv1(session, list_dataset_id: List[str]):
    payload = {
        "list_dataset_id": list_dataset_id,
    }
    result = requests.post(
        session.get_url() + "/ingestion/read_dataset_csvv1",
        json=payload,
        verify=False,
    )
    return result.json()["dataset_id"]
