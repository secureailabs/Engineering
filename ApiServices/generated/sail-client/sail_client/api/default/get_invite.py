from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_invite_out import GetInviteOut
from ...models.http_exception_obj import HTTPExceptionObj
from ...models.validation_error import ValidationError
from ...types import Response


def _get_kwargs(
    organization_id: str,
    invite_id: str,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/data-federations/{organization_id}/invites/{invite_id}".format(
        client.base_url, organization_id=organization_id, invite_id=invite_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[GetInviteOut, HTTPExceptionObj, ValidationError]]:
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failure status code: {response.status_code}. Details: {response.text}")

    if response.status_code == HTTPStatus.OK:
        response_200 = GetInviteOut.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ValidationError.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = HTTPExceptionObj.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = HTTPExceptionObj.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[GetInviteOut, HTTPExceptionObj, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_id: str,
    invite_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[GetInviteOut, HTTPExceptionObj, ValidationError]]:
    """Get Invite

     Get the information about an invite

    Args:
        organization_id (str): UUID of the invired organization
        invite_id (str): UUID of the invite to be fetched

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetInviteOut, HTTPExceptionObj, ValidationError]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        invite_id=invite_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_id: str,
    invite_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GetInviteOut, HTTPExceptionObj, ValidationError]]:
    """Get Invite

     Get the information about an invite

    Args:
        organization_id (str): UUID of the invired organization
        invite_id (str): UUID of the invite to be fetched

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetInviteOut, HTTPExceptionObj, ValidationError]]
    """

    return sync_detailed(
        organization_id=organization_id,
        invite_id=invite_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    organization_id: str,
    invite_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[GetInviteOut, HTTPExceptionObj, ValidationError]]:
    """Get Invite

     Get the information about an invite

    Args:
        organization_id (str): UUID of the invired organization
        invite_id (str): UUID of the invite to be fetched

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetInviteOut, HTTPExceptionObj, ValidationError]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        invite_id=invite_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: str,
    invite_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GetInviteOut, HTTPExceptionObj, ValidationError]]:
    """Get Invite

     Get the information about an invite

    Args:
        organization_id (str): UUID of the invired organization
        invite_id (str): UUID of the invite to be fetched

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetInviteOut, HTTPExceptionObj, ValidationError]]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            invite_id=invite_id,
            client=client,
        )
    ).parsed
