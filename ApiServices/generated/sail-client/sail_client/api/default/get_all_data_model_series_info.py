from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_multiple_data_model_series_out import GetMultipleDataModelSeriesOut
from ...models.validation_error import ValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    data_model_dataframe_id: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/data-models-series".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["data_model_dataframe_id"] = data_model_dataframe_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[GetMultipleDataModelSeriesOut, ValidationError]]:
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failure status code: {response.status_code}. Details: {response.text}")

    if response.status_code == HTTPStatus.OK:
        response_200 = GetMultipleDataModelSeriesOut.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[GetMultipleDataModelSeriesOut, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    data_model_dataframe_id: Union[Unset, None, str] = UNSET,
) -> Response[Union[GetMultipleDataModelSeriesOut, ValidationError]]:
    """Get All Data Model Series Info

     Get all data model series SCNs

    Args:
        data_model_dataframe_id (Union[Unset, None, str]): Data model Id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetMultipleDataModelSeriesOut, ValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        data_model_dataframe_id=data_model_dataframe_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    data_model_dataframe_id: Union[Unset, None, str] = UNSET,
) -> Optional[Union[GetMultipleDataModelSeriesOut, ValidationError]]:
    """Get All Data Model Series Info

     Get all data model series SCNs

    Args:
        data_model_dataframe_id (Union[Unset, None, str]): Data model Id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetMultipleDataModelSeriesOut, ValidationError]]
    """

    return sync_detailed(
        client=client,
        data_model_dataframe_id=data_model_dataframe_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    data_model_dataframe_id: Union[Unset, None, str] = UNSET,
) -> Response[Union[GetMultipleDataModelSeriesOut, ValidationError]]:
    """Get All Data Model Series Info

     Get all data model series SCNs

    Args:
        data_model_dataframe_id (Union[Unset, None, str]): Data model Id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetMultipleDataModelSeriesOut, ValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        data_model_dataframe_id=data_model_dataframe_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    data_model_dataframe_id: Union[Unset, None, str] = UNSET,
) -> Optional[Union[GetMultipleDataModelSeriesOut, ValidationError]]:
    """Get All Data Model Series Info

     Get all data model series SCNs

    Args:
        data_model_dataframe_id (Union[Unset, None, str]): Data model Id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetMultipleDataModelSeriesOut, ValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            data_model_dataframe_id=data_model_dataframe_id,
        )
    ).parsed
