from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.http_exception_obj import HTTPExceptionObj
from ...models.register_organization_in import RegisterOrganizationIn
from ...models.register_organization_out import RegisterOrganizationOut
from ...models.validation_error import ValidationError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: RegisterOrganizationIn,
) -> Dict[str, Any]:
    url = "{}/organizations".format(client.base_url)

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
) -> Optional[Union[HTTPExceptionObj, RegisterOrganizationOut, ValidationError]]:
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failure status code: {response.status_code}. Details: {response.text}")

    if response.status_code == HTTPStatus.CREATED:
        response_201 = RegisterOrganizationOut.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ValidationError.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.CONFLICT:
        response_409 = HTTPExceptionObj.from_dict(response.json())

        return response_409
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[HTTPExceptionObj, RegisterOrganizationOut, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: RegisterOrganizationIn,
) -> Response[Union[HTTPExceptionObj, RegisterOrganizationOut, ValidationError]]:
    """Register Organization

     Register new organization and the admin user

    Args:
        json_body (RegisterOrganizationIn): Organization details

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPExceptionObj, RegisterOrganizationOut, ValidationError]]
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
    client: Client,
    json_body: RegisterOrganizationIn,
) -> Optional[Union[HTTPExceptionObj, RegisterOrganizationOut, ValidationError]]:
    """Register Organization

     Register new organization and the admin user

    Args:
        json_body (RegisterOrganizationIn): Organization details

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPExceptionObj, RegisterOrganizationOut, ValidationError]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: RegisterOrganizationIn,
) -> Response[Union[HTTPExceptionObj, RegisterOrganizationOut, ValidationError]]:
    """Register Organization

     Register new organization and the admin user

    Args:
        json_body (RegisterOrganizationIn): Organization details

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPExceptionObj, RegisterOrganizationOut, ValidationError]]
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
    client: Client,
    json_body: RegisterOrganizationIn,
) -> Optional[Union[HTTPExceptionObj, RegisterOrganizationOut, ValidationError]]:
    """Register Organization

     Register new organization and the admin user

    Args:
        json_body (RegisterOrganizationIn): Organization details

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPExceptionObj, RegisterOrganizationOut, ValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
