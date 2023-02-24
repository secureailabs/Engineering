import requests


def histogram(session, series_1_id, bin_count):
    payload = {
        "series_1_id": series_1_id,
        "bin_count": bin_count,
    }
    result = requests.post(session.get_url() + "/visualization/histogram/", params=payload, verify=False)
    return result.json()


def kernel_density_estimation(session, series_1_id: str, bin_size: float):
    payload = {
        "series_1_id": series_1_id,
        "bin_size": bin_size,
    }
    result = requests.post(
        session.get_url() + "/visualization/kernel_density_estimation/",
        params=payload,
        verify=False,
    )
    return result.json()
