import json
import logging
import os
import threading
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from log.audit_log import _AsyncLogger, log_message
from pydantic import BaseModel
from sail_core.implementation.participant_service_client_dict import ParticipantServiceClientDict
from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator import preprocessing, statistics, visualization
from sail_safe_functions.aggregator.client_rpc_zero import ClientRPCZero
from sail_safe_functions.aggregator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions.test.helper_sail_safe_functions.test_service_reference import TestServiceReference

app = FastAPI()

service_reference = TestServiceReference.get_instance()

dataframe_name_lookup = {}

scn_names = []
scn_ports = []
list_dataset_id = []

IV_SETTINGS_FILE = "/app/InitializationVector.json"

if os.environ.get("IV_FILEPATH") is not None:
    IV_SETTINGS_FILE = os.environ.get("IV_FILEPATH")

with open(IV_SETTINGS_FILE) as initial_settings:
    configuration = json.load(initial_settings)
    for entry in configuration["secure_computation_nodes"]:
        scn_names.append(entry["ip_address"])
        scn_ports.append(5556)
        list_dataset_id.append(entry["dataset_id"])


# TODO make this a other implementation that autoconfigures
participant_service = ParticipantServiceClientDict()
for dataset_id, scn_name, scn_port in zip(list_dataset_id, scn_names, scn_ports):
    participant_service.register_client(dataset_id, ClientRPCZero(scn_name, scn_port))
    print(f"Connected to SCN {scn_name} serving dataset {dataset_id}")


implementation_manager = ImplementationManager.get_instance()
implementation_manager.set_participant_service(participant_service)
implementation_manager.initialize()


class Audit_log_task(threading.Thread):
    """
    Auxillary class for audit log server in isolated thread
    """

    def run(self):
        """
        Start async logger server
        """
        _AsyncLogger.start_log_poller(_AsyncLogger.ipc, _AsyncLogger.port)


@app.on_event("startup")
async def start_audit_logger():
    """
    Start async audit logger server at start up as a background task
    """
    t = Audit_log_task()
    t.start()


async def log_validation_failure(message):
    logger = logging.getLogger("uvicorn.error")
    logger.error(message)
    await log_message(message)


@app.get("/")
async def root():
    """
    Redirects user to docs as hompage
    """
    return RedirectResponse("/docs")


def get_series(series_uuid: str):
    return service_reference.reference_to_federated_series(series_uuid)


def get_dataframe(dataframe_uuid: str):
    return service_reference.reference_to_federated_dataframe(dataframe_uuid)


def query_limit_n(series, n=10) -> bool:
    """
    Checks data or series in question is over a given threshold.

    :param: data: the data item being checked
    :type: remote dataframe or remote series
    :return: True or False relating to whether the threshold has been surpassed
    :type: Boolean
    """
    return statistics.count(series) > n


async def validate(series):
    """
    Validates execution criteria for data inputs
    :param: data: the data item being validated
    :type: Remote Dataframe or Remote Series
    :return: None
    :type: None
    """
    if not query_limit_n(series):
        message = "Validation Failure: Sample size too small"
        await log_validation_failure(message)
        raise HTTPException(status_code=500, detail=message)
    else:
        return

    # CHECKS
    # TODO:
    #       1. Check for pandas query injection in column_id string
    # CLOSE CHECKS


@app.post("/admin/get_dataframe_name_lookup_table")
async def get_dataframe_name_lookup_table() -> dict:
    return {"dataframe_name_lookup": dataframe_name_lookup}


# DATA MODEL


@app.post("/data_model/new_tabular_model")
async def data_frame_tabular() -> dict:
    data_frame_tabular = DataModelTabular()
    data_frame_id = service_reference.get_instance().data_model_tabular_to_reference(data_frame_tabular)

    return {"data_frame_tabular_id": data_frame_id}


@app.post("/data_model/new_series_model_numerical")
async def new_series_numerical(series_name: str, measurement_source_name: str, type_agregator: str, unit: str) -> dict:

    series = DataModelSeries.create_numerical(
        series_name=series_name,
        measurement_source_name=measurement_source_name,
        type_agregator=type_agregator,
        unit=unit,
    )
    series_ref = service_reference.get_instance().data_model_series_to_reference(series)

    return {"series": series_ref}


@app.post("/data_model/tabular/{data_model_tabular_id}/add_dataframe")
async def tabular_model_add_dataframe_model(data_model_tabular_id: str, data_model_dataframe_id: str) -> dict:
    data_model_tabular = service_reference.get_instance().reference_to_data_model_tabular(data_model_tabular_id)
    data_model = service_reference.get_instance().reference_to_data_model_data_frame(data_model_dataframe_id)

    data_model_tabular.add_data_model_data_frame(data_model)

    return {"data_frame_tabular_id": data_model_tabular_id}


@app.post("/data_model/new_data_frame_model")
async def create_data_model_data_frame(data_frame_name: str) -> dict:
    dataframe_id = ""
    if data_frame_name not in dataframe_name_lookup:
        new_dataframe = DataModelDataFrame(data_frame_name)
        dataframe_id = service_reference.get_instance().data_model_data_frame_to_reference(new_dataframe)
        dataframe_name_lookup[data_frame_name] = dataframe_id
    else:
        dataframe_id = dataframe_name_lookup[data_frame_name]

    return {"data_model_id": dataframe_id}


@app.post("/data_model/data_frame/{data_model_id}/add_new_series_model")
async def data_model_add_series_model(
    data_model_id: str,
    series_name: str,
    measurement_source_name: str,
    type_agregator: str,
) -> dict:
    data_model_data_frame = service_reference.get_instance().reference_to_data_model_data_frame(data_model_id)
    if data_model_data_frame is not None:
        data_model_data_frame.add_data_model_series(
            DataModelSeries.create_numerical(
                series_name=series_name,
                measurement_source_name=measurement_source_name,
                type_agregator=type_agregator,
                unit="kg/m2",
            )
        )

    return {"data_model_id": data_model_id}


# DATA MODEL END
# DATA INGESTION
@app.post("/ingestion/read_longitudinal/fhirv1")
async def read_longitudinal_fhirv1() -> dict:
    dataset_longitudinal = preprocessing.read_dataset_fhirv1(list_dataset_id)

    longitudinal_id = service_reference.get_instance().federated_longitudinal_data_to_reference(dataset_longitudinal)

    return {"longitudinal_id": longitudinal_id}


@app.post("/ingestion/read_dataset_tabular_from_longitudinal")
async def read_dataset_tabular_from_longitudinal(
    longitudinal_id: str,
    dataset_federation_id: str,
    dataset_federation_name: str,
    data_model_tabular_id: str,
) -> dict:
    dataset_longitudinal = service_reference.get_instance().reference_to_federated_longitudinal_data(longitudinal_id)

    data_model_tablular = service_reference.get_instance().reference_to_data_model_tabular(data_model_tabular_id)

    dataset_tabular = preprocessing.convert_to_dataset_tabular(
        dataset_longitudinal,
        dataset_federation_id,
        dataset_federation_name,
        data_model_tablular,
    )

    dataset_id = service_reference.get_instance().data_set_tabular_to_reference(dataset_tabular)

    return {"dataset_id": dataset_id}


@app.post("/ingestion/dataset_tabular/fhirv1")
async def dataset_tabular_fhirv1(
    dataset_federation_id: str, dataset_federation_name: str, data_model_tabular_id: str
) -> dict:
    dataset_longitudinal = preprocessing.read_dataset_fhirv1(list_dataset_id)
    data_model_tablular = service_reference.get_instance().reference_to_data_model_tabular(data_model_tabular_id)

    dataset_tabular = preprocessing.convert_to_dataset_tabular(
        dataset_longitudinal,
        dataset_federation_id,
        dataset_federation_name,
        data_model_tablular,
    )

    dataset_id = service_reference.get_instance().data_set_tabular_to_reference(dataset_tabular)

    return {"dataset_id": dataset_id}


class DataFederation(BaseModel):
    list_dataset_id: List[str]


@app.post("/ingestion/read_dataset_csvv1")
async def read_dataset_csvv1(data_federation: DataFederation) -> dict:
    list_dataset_id = data_federation.list_dataset_id
    dataset_tabular = preprocessing.read_dataset_csvv1(list_dataset_id)
    dataset_id = service_reference.get_instance().data_set_tabular_to_reference(dataset_tabular)
    return {"dataset_id": dataset_id}


# DATA INGESTION END
# DATAFRAME MANIPULATION


@app.post("/data_frame_tabular/select_dataframe/{data_frame_tabular_id}")
async def data_frame_tabular_select_dataframe(data_frame_tabular_id: str, data_frame_name: str) -> dict:
    data_frame_tabular = service_reference.get_instance().reference_to_data_set_tabular(data_frame_tabular_id)
    data_frame = data_frame_tabular[data_frame_name]

    data_frame_id = service_reference.get_instance().federated_dataframe_to_reference(data_frame)
    return {"data_frame_id": data_frame_id}


@app.post("/data_frame/select_series/{data_frame_id}")
async def data_frame_select_series(data_frame_id: str, series_name: str) -> dict:
    data_frame = service_reference.get_instance().reference_to_federated_dataframe(data_frame_id)
    series = data_frame[series_name]

    series_id = service_reference.get_instance().federated_series_to_reference(series)
    return {"series_id": series_id}


# DATAFRAME_MANIPULATION END

# PREPROCESSING
# Doesn't work but we should allow it
# @app.post("/preprocessing/series/drop_missing/{series_id}")
# async def series_drop_missing(series_id: str) -> dict:
#     orig_series = service_reference.get_instance().reference_to_federated_series(
#         series_id
#     )
#     new_series = preprocessing.drop_missing(
#         orig_series, axis=0, how="any", thresh=None, subset=None
#     )

#     new_series_id = service_reference.get_instance().federated_series_to_reference(
#         new_series
#     )

#     return {"series_id": new_series_id}


@app.post("/preprocessing/data_frame/drop_missing/{dataset_id}")
async def series_drop_missing(dataset_id: str) -> dict:
    orig_data_frame = service_reference.get_instance().reference_to_federated_dataframe(dataset_id)
    new_data_frame = preprocessing.drop_missing(orig_data_frame, axis=0, how="any", thresh=None, subset=None)

    new_data_frame_id = service_reference.get_instance().federated_dataframe_to_reference(new_data_frame)

    return {"result_data_frame_id": new_data_frame_id}


@app.post("/preprocessing/data_frame/query/{data_frame_id}")
async def data_frame_query(data_frame_id: str, query_str: str) -> dict:
    orig_data_frame = service_reference.get_instance().reference_to_federated_dataframe(data_frame_id)
    new_data_frame = preprocessing.query(orig_data_frame, query_str)

    new_data_frame_id = service_reference.get_instance().federated_dataframe_to_reference(new_data_frame)

    return {"result_data_frame_id": new_data_frame_id}


# END PREPROCESSING

# STATS


@app.post("/statistics/chisquare/{series_1_id}/{series_2_id}")
async def chisquare(series_1_id: str, series_2_id: str) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)

    return {"chisquare": statistics.chisquare(series_1, series_2)}


@app.post("/statistics/count/{series_id}")
async def count(series_id: str) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)

    await validate(series)
    return {"count": statistics.count(series)}


@app.post("/statistics/kolmogorovSmirnovTest/{series_1_id}")
async def kolmogorovSmirnovTest(series_1_id: str, type_distribution: str, type_ranking: str) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_1_id)

    await validate(series)
    return {"kolmogorov_smirnov_test": statistics.kolmogorov_smirnov_test(series, type_distribution, type_ranking)}


@app.post("/statistics/kurtosis/{series_id}")
async def kurtosis(series_id: str) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)
    await validate(series)
    return {"kurtosis": statistics.kurtosis(series)}


@app.post("/statistics/levene_test/{series_1_id}/{series_2_id}")
async def levene_test(series_1_id: str, series_2_id: str) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)

    f_statistic_sail, p_value_sail = statistics.levene_test(series_1, series_2)

    return {"f_statistic": f_statistic_sail, "p_value": p_value_sail}


@app.post("/statistics/mann_whitney_u_test/{series_1_id}/{series_2_id}")
async def mann_whitney_u_test(series_1_id: str, series_2_id: str, alternative: str, type_ranking: str) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)

    w_statistic_sail, p_value_sail = statistics.mann_whitney_u_test(series_1, series_2, alternative, type_ranking)
    return {"w_statistic": w_statistic_sail, "p_value": p_value_sail}


@app.post("/statistics/mean/{series_id}")
async def mean(series_id: str) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)

    await validate(series)

    return {"mean": statistics.mean(series)}


@app.post("/statistics/min_max/{series_id}")
async def min_max(series_id: str) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)

    await validate(series)

    min, max = statistics.min_max(series)
    return {"min": min, "max": max}


@app.post("/statistics/paired_t_test/{series_1_id}/{series_2_id}")
async def paired_t_test(series_1_id: str, series_2_id: str, alternative: str) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)

    t_statistic_sail, p_value_sail = statistics.paired_t_test(series_1, series_2, alternative)
    return {"t_statistic": t_statistic_sail, "p_value": p_value_sail}


@app.post("/statistics/pearson/{series_1_id}/{series_2_id}")
async def pearson(series_1_id: str, series_2_id: str, alternative: str) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)

    pearson_sail, p_value_sail = statistics.pearson(series_1, series_2, alternative)
    return {"pearson": pearson_sail, "p_value": p_value_sail}


@app.post("/statistics/skewness/{series_id}")
async def skewness(series_id: str) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)
    await validate(series)

    return {"skewness": statistics.skewness(series)}


@app.post("/statistics/spearman/{series_1_id}/{series_2_id}")
async def spearman(series_1_id: str, series_2_id: str, alternative: str, type_ranking: str) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)
    spearman_sail, p_value_sail = statistics.spearman(series_1, series_2, alternative, type_ranking)
    return {"spearman": spearman_sail, "p_value": p_value_sail}


@app.post("/statistics/student_t_test/{series_1_id}/{series_2_id}")
async def student_t_test(series_1_id: str, series_2_id: str, alternative: str) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)

    t_statistic_sail, p_value_sail = statistics.student_t_test(series_1, series_2, alternative)
    return {"t_statistic": t_statistic_sail, "p_value": p_value_sail}


@app.post("/statistics/variance/{series_id}")
async def variance(series_id: str) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)
    await validate(series)

    return {"variance": statistics.variance(series)}


@app.post("/statistics/welch_t_test/{series_1_id}/{series_2_id}")
async def welch_t_test(series_1_id: str, series_2_id: str, alternative: str) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)

    t_statistic_sail, p_value_sail = statistics.welch_t_test(series_1, series_2, alternative)
    return {"t_statistic": t_statistic_sail, "p_value": p_value_sail}


@app.post("/statistics/wilcoxon_signed_rank_test/{series_1_id}/{series_2_id}")
async def wilcoxon_signed_rank_test(series_1_id: str, series_2_id: str, alternative: str, type_ranking: str) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)

    w_statistic_sail, p_value_sail = statistics.spearman(series_1, series_2, alternative, type_ranking)
    return {"w_statistic": w_statistic_sail, "p_value": p_value_sail}


# END STATS

# START VISUALIZATION


@app.post("/visualization/histogram/")
async def histogram_federated(series_1_id: str, bin_count: int) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)

    await validate(series_1)

    figure = visualization.histogram_federated(series_1, bin_count)

    return {"figure": figure}


@app.post("/visualization/kernel_density_estimation/")
async def kernel_density_estimation(series_1_id: str, bin_size: float) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)

    await validate(series_1)

    figure = visualization.kernel_density_estimation(series_1, bin_size)

    return {"figure": figure}


# END VISUALIZATION
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
