from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_multiple_secure_computation_node_out import GetMultipleSecureComputationNodeOut
from ...models.http_exception_obj import HTTPExceptionObj
from ...models.validation_error import ValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    data_federation_provision_id: str,
) -> Dict[str, Any]:
    url = "{}/secure-computation-node".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["data_federation_provision_id"] = data_federation_provision_id

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
) -> Optional[Union[GetMultipleSecureComputationNodeOut, HTTPExceptionObj, ValidationError]]:
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failure status code: {response.status_code}. Details: {response.text}")

    if response.status_code == HTTPStatus.OK:
        response_200 = GetMultipleSecureComputationNodeOut.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ValidationError.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = HTTPExceptionObj.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[GetMultipleSecureComputationNodeOut, HTTPExceptionObj, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    data_federation_provision_id: str,
) -> Response[Union[GetMultipleSecureComputationNodeOut, HTTPExceptionObj, ValidationError]]:
    """Get All Secure Computation Nodes

     Get list of all the secure_computation_node for the current user and federation provision

    Args:
        data_federation_provision_id (str): Data federation provision id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetMultipleSecureComputationNodeOut, HTTPExceptionObj, ValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        data_federation_provision_id=data_federation_provision_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    data_federation_provision_id: str,
) -> Optional[Union[GetMultipleSecureComputationNodeOut, HTTPExceptionObj, ValidationError]]:
    """Get All Secure Computation Nodes

     Get list of all the secure_computation_node for the current user and federation provision

    Args:
        data_federation_provision_id (str): Data federation provision id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetMultipleSecureComputationNodeOut, HTTPExceptionObj, ValidationError]]
    """

    return sync_detailed(
        client=client,
        data_federation_provision_id=data_federation_provision_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    data_federation_provision_id: str,
) -> Response[Union[GetMultipleSecureComputationNodeOut, HTTPExceptionObj, ValidationError]]:
    """Get All Secure Computation Nodes

     Get list of all the secure_computation_node for the current user and federation provision

    Args:
        data_federation_provision_id (str): Data federation provision id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetMultipleSecureComputationNodeOut, HTTPExceptionObj, ValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        data_federation_provision_id=data_federation_provision_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    data_federation_provision_id: str,
) -> Optional[Union[GetMultipleSecureComputationNodeOut, HTTPExceptionObj, ValidationError]]:
    """Get All Secure Computation Nodes

     Get list of all the secure_computation_node for the current user and federation provision

    Args:
        data_federation_provision_id (str): Data federation provision id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetMultipleSecureComputationNodeOut, HTTPExceptionObj, ValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            data_federation_provision_id=data_federation_provision_id,
        )
    ).parsed
