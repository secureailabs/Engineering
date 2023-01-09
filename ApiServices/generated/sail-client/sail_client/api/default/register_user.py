from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_exception_obj import HTTPExceptionObj
from ...models.register_user_in import RegisterUserIn
from ...models.register_user_out import RegisterUserOut
from ...models.validation_error import ValidationError
from ...types import Response


def _get_kwargs(
    organization_id: str,
    *,
    client: AuthenticatedClient,
    json_body: RegisterUserIn,
) -> Dict[str, Any]:
    url = "{}/organizations/{organization_id}/users".format(client.base_url, organization_id=organization_id)

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
) -> Optional[Union[HTTPExceptionObj, RegisterUserOut, ValidationError]]:

    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failure status code: {response.status_code}. Details: {response.text}")

    if response.status_code == HTTPStatus.CREATED:
        response_201 = RegisterUserOut.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ValidationError.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = HTTPExceptionObj.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.CONFLICT:
        response_409 = HTTPExceptionObj.from_dict(response.json())

        return response_409
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[HTTPExceptionObj, RegisterUserOut, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_id: str,
    *,
    client: AuthenticatedClient,
    json_body: RegisterUserIn,
) -> Response[Union[HTTPExceptionObj, RegisterUserOut, ValidationError]]:
    """Register User

     Add new user to organization

    Args:
        organization_id (str): UUID of the organization to add the user to
        json_body (RegisterUserIn): User details to register with the organization

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPExceptionObj, RegisterUserOut, ValidationError]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_id: str,
    *,
    client: AuthenticatedClient,
    json_body: RegisterUserIn,
) -> Optional[Union[HTTPExceptionObj, RegisterUserOut, ValidationError]]:
    """Register User

     Add new user to organization

    Args:
        organization_id (str): UUID of the organization to add the user to
        json_body (RegisterUserIn): User details to register with the organization

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPExceptionObj, RegisterUserOut, ValidationError]]
    """

    return sync_detailed(
        organization_id=organization_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    organization_id: str,
    *,
    client: AuthenticatedClient,
    json_body: RegisterUserIn,
) -> Response[Union[HTTPExceptionObj, RegisterUserOut, ValidationError]]:
    """Register User

     Add new user to organization

    Args:
        organization_id (str): UUID of the organization to add the user to
        json_body (RegisterUserIn): User details to register with the organization

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPExceptionObj, RegisterUserOut, ValidationError]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: str,
    *,
    client: AuthenticatedClient,
    json_body: RegisterUserIn,
) -> Optional[Union[HTTPExceptionObj, RegisterUserOut, ValidationError]]:
    """Register User

     Add new user to organization

    Args:
        organization_id (str): UUID of the organization to add the user to
        json_body (RegisterUserIn): User details to register with the organization

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPExceptionObj, RegisterUserOut, ValidationError]]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
