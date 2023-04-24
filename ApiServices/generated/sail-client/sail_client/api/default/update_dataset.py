from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_exception_obj import HTTPExceptionObj
from ...models.update_dataset_in import UpdateDatasetIn
from ...models.validation_error import ValidationError
from ...types import Response


def _get_kwargs(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    json_body: UpdateDatasetIn,
) -> Dict[str, Any]:
    url = "{}/datasets/{dataset_id}".format(client.base_url, dataset_id=dataset_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[HTTPExceptionObj, None, ValidationError]]:
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failure status code: {response.status_code}. Details: {response.text}")

    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(None, None)
        return response_204
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ValidationError.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = HTTPExceptionObj.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = HTTPExceptionObj.from_dict(response.json())

        return response_403
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[HTTPExceptionObj, None, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    json_body: UpdateDatasetIn,
) -> Response[Union[HTTPExceptionObj, None, ValidationError]]:
    """Update Dataset

     Update dataset information

    Args:
        dataset_id (str): UUID of the dataset being updated
        json_body (UpdateDatasetIn): Updated dataset information

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPExceptionObj, None, ValidationError]]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    json_body: UpdateDatasetIn,
) -> Optional[Union[HTTPExceptionObj, None, ValidationError]]:
    """Update Dataset

     Update dataset information

    Args:
        dataset_id (str): UUID of the dataset being updated
        json_body (UpdateDatasetIn): Updated dataset information

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPExceptionObj, None, ValidationError]]
    """

    return sync_detailed(
        dataset_id=dataset_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    json_body: UpdateDatasetIn,
) -> Response[Union[HTTPExceptionObj, None, ValidationError]]:
    """Update Dataset

     Update dataset information

    Args:
        dataset_id (str): UUID of the dataset being updated
        json_body (UpdateDatasetIn): Updated dataset information

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPExceptionObj, None, ValidationError]]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    json_body: UpdateDatasetIn,
) -> Optional[Union[HTTPExceptionObj, None, ValidationError]]:
    """Update Dataset

     Update dataset information

    Args:
        dataset_id (str): UUID of the dataset being updated
        json_body (UpdateDatasetIn): Updated dataset information

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPExceptionObj, None, ValidationError]]
    """

    return (
        await asyncio_detailed(
            dataset_id=dataset_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
