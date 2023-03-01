import requests


def drop_na_data_frame(session, data_frame_id):
    payload = {"data_frame_id": data_frame_id}
    result = requests.post(
        session.get_url() + "/preprocessing/data_frame/drop_missing/" + data_frame_id,
        params=payload,
        verify=False,
    )
    return result.json()["result_data_frame_id"]


def query_data_frame(session, data_frame_id, query):
    payload = {"query_str": query}
    result = requests.post(
        session.get_url() + "/preprocessing/data_frame/query/" + data_frame_id,
        params=payload,
        verify=False,
    )
    return result.json()["result_data_frame_id"]


# NOTE: Doesn't work but we should allow it
# def drop_na_series(session, series_id):
#     payload = {"series_id": series_id}
#     result = requests.post(
#         "http://"
#         + session.ip
#         + ":"
#         + session.port
#         + "/preprocessing/series/drop_missing/"
#         + series_id,
#         params=payload,
#     )
#     return result.json()["series_id"]
