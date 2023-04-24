from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.register_data_model_dataframe_in import RegisterDataModelDataframeIn
from ...models.register_data_model_dataframe_out import RegisterDataModelDataframeOut
from ...models.validation_error import ValidationError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: RegisterDataModelDataframeIn,
) -> Dict[str, Any]:
    url = "{}/data-models-dataframes".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[RegisterDataModelDataframeOut, ValidationError]]:
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failure status code: {response.status_code}. Details: {response.text}")

    if response.status_code == HTTPStatus.CREATED:
        response_201 = RegisterDataModelDataframeOut.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[RegisterDataModelDataframeOut, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: RegisterDataModelDataframeIn,
) -> Response[Union[RegisterDataModelDataframeOut, ValidationError]]:
    """Register Data Model Dataframe

     Provision data federation SCNs

    Args:
        json_body (RegisterDataModelDataframeIn): Information required for creating data model
            dataframe

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RegisterDataModelDataframeOut, ValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: RegisterDataModelDataframeIn,
) -> Optional[Union[RegisterDataModelDataframeOut, ValidationError]]:
    """Register Data Model Dataframe

     Provision data federation SCNs

    Args:
        json_body (RegisterDataModelDataframeIn): Information required for creating data model
            dataframe

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RegisterDataModelDataframeOut, ValidationError]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: RegisterDataModelDataframeIn,
) -> Response[Union[RegisterDataModelDataframeOut, ValidationError]]:
    """Register Data Model Dataframe

     Provision data federation SCNs

    Args:
        json_body (RegisterDataModelDataframeIn): Information required for creating data model
            dataframe

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RegisterDataModelDataframeOut, ValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: RegisterDataModelDataframeIn,
) -> Optional[Union[RegisterDataModelDataframeOut, ValidationError]]:
    """Register Data Model Dataframe

     Provision data federation SCNs

    Args:
        json_body (RegisterDataModelDataframeIn): Information required for creating data model
            dataframe

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RegisterDataModelDataframeOut, ValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
