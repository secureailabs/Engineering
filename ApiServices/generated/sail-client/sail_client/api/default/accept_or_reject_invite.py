from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_exception_obj import HTTPExceptionObj
from ...models.patch_invite_in import PatchInviteIn
from ...models.validation_error import ValidationError
from ...types import Response


def _get_kwargs(
    organization_id: str,
    invite_id: str,
    *,
    client: AuthenticatedClient,
    json_body: PatchInviteIn,
) -> Dict[str, Any]:
    url = "{}/data-federations/{organization_id}/invites/{invite_id}".format(
        client.base_url, organization_id=organization_id, invite_id=invite_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "patch",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[Any, HTTPExceptionObj, ValidationError]]:

    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failure status code: {response.status_code}. Details: {response.text}")

    if response.status_code == HTTPStatus.OK:
        response_200 = cast(Any, response.json())
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
    if response.status_code == HTTPStatus.GONE:
        response_410 = HTTPExceptionObj.from_dict(response.json())

        return response_410
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, HTTPExceptionObj, ValidationError]]:
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
    json_body: PatchInviteIn,
) -> Response[Union[Any, HTTPExceptionObj, ValidationError]]:
    """Accept Or Reject Invite

     Accept or reject an invite

    Args:
        organization_id (str): UUID of the invited organization
        invite_id (str): UUID of the invite to be approved to rejected
        json_body (PatchInviteIn): The accpet or reject information

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPExceptionObj, ValidationError]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        invite_id=invite_id,
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
    invite_id: str,
    *,
    client: AuthenticatedClient,
    json_body: PatchInviteIn,
) -> Optional[Union[Any, HTTPExceptionObj, ValidationError]]:
    """Accept Or Reject Invite

     Accept or reject an invite

    Args:
        organization_id (str): UUID of the invited organization
        invite_id (str): UUID of the invite to be approved to rejected
        json_body (PatchInviteIn): The accpet or reject information

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPExceptionObj, ValidationError]]
    """

    return sync_detailed(
        organization_id=organization_id,
        invite_id=invite_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    organization_id: str,
    invite_id: str,
    *,
    client: AuthenticatedClient,
    json_body: PatchInviteIn,
) -> Response[Union[Any, HTTPExceptionObj, ValidationError]]:
    """Accept Or Reject Invite

     Accept or reject an invite

    Args:
        organization_id (str): UUID of the invited organization
        invite_id (str): UUID of the invite to be approved to rejected
        json_body (PatchInviteIn): The accpet or reject information

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPExceptionObj, ValidationError]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        invite_id=invite_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: str,
    invite_id: str,
    *,
    client: AuthenticatedClient,
    json_body: PatchInviteIn,
) -> Optional[Union[Any, HTTPExceptionObj, ValidationError]]:
    """Accept Or Reject Invite

     Accept or reject an invite

    Args:
        organization_id (str): UUID of the invited organization
        invite_id (str): UUID of the invite to be approved to rejected
        json_body (PatchInviteIn): The accpet or reject information

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPExceptionObj, ValidationError]]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            invite_id=invite_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
