from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_exception_obj import HTTPExceptionObj
from ...models.query_result import QueryResult
from ...models.validation_error import ValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    label: str,
    user_id: Union[Unset, None, str] = UNSET,
    data_id: Union[Unset, None, str] = UNSET,
    start: Union[None, Unset, float, int] = UNSET,
    end: Union[None, Unset, float, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    step: Union[Unset, None, str] = UNSET,
    direction: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/audit-logs".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["label"] = label

    params["user_id"] = user_id

    params["data_id"] = data_id

    json_start: Union[None, Unset, float, int]
    if isinstance(start, Unset):
        json_start = UNSET
    elif start is None:
        json_start = None

    else:
        json_start = start

    params["start"] = json_start

    json_end: Union[None, Unset, float, int]
    if isinstance(end, Unset):
        json_end = UNSET
    elif end is None:
        json_end = None

    else:
        json_end = end

    params["end"] = json_end

    params["limit"] = limit

    params["step"] = step

    params["direction"] = direction

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
) -> Optional[Union[HTTPExceptionObj, QueryResult, ValidationError]]:
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failure status code: {response.status_code}. Details: {response.text}")

    if response.status_code == HTTPStatus.OK:
        response_200 = QueryResult.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ValidationError.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = HTTPExceptionObj.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = HTTPExceptionObj.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[HTTPExceptionObj, QueryResult, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    label: str,
    user_id: Union[Unset, None, str] = UNSET,
    data_id: Union[Unset, None, str] = UNSET,
    start: Union[None, Unset, float, int] = UNSET,
    end: Union[None, Unset, float, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    step: Union[Unset, None, str] = UNSET,
    direction: Union[Unset, None, str] = UNSET,
) -> Response[Union[HTTPExceptionObj, QueryResult, ValidationError]]:
    """Audit Incidents Query

     query by logQL

    Args:
        label (str):
        user_id (Union[Unset, None, str]): query events related to a specific user id
        data_id (Union[Unset, None, str]): query events related to a specific data id
        start (Union[None, Unset, float, int]): starting timestamp of the query range
        end (Union[None, Unset, float, int]): ending timestamp of the query range
        limit (Union[Unset, None, int]): query events number limit
        step (Union[Unset, None, str]): query events time interval
        direction (Union[Unset, None, str]): query events order

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPExceptionObj, QueryResult, ValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        label=label,
        user_id=user_id,
        data_id=data_id,
        start=start,
        end=end,
        limit=limit,
        step=step,
        direction=direction,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    label: str,
    user_id: Union[Unset, None, str] = UNSET,
    data_id: Union[Unset, None, str] = UNSET,
    start: Union[None, Unset, float, int] = UNSET,
    end: Union[None, Unset, float, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    step: Union[Unset, None, str] = UNSET,
    direction: Union[Unset, None, str] = UNSET,
) -> Optional[Union[HTTPExceptionObj, QueryResult, ValidationError]]:
    """Audit Incidents Query

     query by logQL

    Args:
        label (str):
        user_id (Union[Unset, None, str]): query events related to a specific user id
        data_id (Union[Unset, None, str]): query events related to a specific data id
        start (Union[None, Unset, float, int]): starting timestamp of the query range
        end (Union[None, Unset, float, int]): ending timestamp of the query range
        limit (Union[Unset, None, int]): query events number limit
        step (Union[Unset, None, str]): query events time interval
        direction (Union[Unset, None, str]): query events order

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPExceptionObj, QueryResult, ValidationError]]
    """

    return sync_detailed(
        client=client,
        label=label,
        user_id=user_id,
        data_id=data_id,
        start=start,
        end=end,
        limit=limit,
        step=step,
        direction=direction,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    label: str,
    user_id: Union[Unset, None, str] = UNSET,
    data_id: Union[Unset, None, str] = UNSET,
    start: Union[None, Unset, float, int] = UNSET,
    end: Union[None, Unset, float, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    step: Union[Unset, None, str] = UNSET,
    direction: Union[Unset, None, str] = UNSET,
) -> Response[Union[HTTPExceptionObj, QueryResult, ValidationError]]:
    """Audit Incidents Query

     query by logQL

    Args:
        label (str):
        user_id (Union[Unset, None, str]): query events related to a specific user id
        data_id (Union[Unset, None, str]): query events related to a specific data id
        start (Union[None, Unset, float, int]): starting timestamp of the query range
        end (Union[None, Unset, float, int]): ending timestamp of the query range
        limit (Union[Unset, None, int]): query events number limit
        step (Union[Unset, None, str]): query events time interval
        direction (Union[Unset, None, str]): query events order

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPExceptionObj, QueryResult, ValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        label=label,
        user_id=user_id,
        data_id=data_id,
        start=start,
        end=end,
        limit=limit,
        step=step,
        direction=direction,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    label: str,
    user_id: Union[Unset, None, str] = UNSET,
    data_id: Union[Unset, None, str] = UNSET,
    start: Union[None, Unset, float, int] = UNSET,
    end: Union[None, Unset, float, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    step: Union[Unset, None, str] = UNSET,
    direction: Union[Unset, None, str] = UNSET,
) -> Optional[Union[HTTPExceptionObj, QueryResult, ValidationError]]:
    """Audit Incidents Query

     query by logQL

    Args:
        label (str):
        user_id (Union[Unset, None, str]): query events related to a specific user id
        data_id (Union[Unset, None, str]): query events related to a specific data id
        start (Union[None, Unset, float, int]): starting timestamp of the query range
        end (Union[None, Unset, float, int]): ending timestamp of the query range
        limit (Union[Unset, None, int]): query events number limit
        step (Union[Unset, None, str]): query events time interval
        direction (Union[Unset, None, str]): query events order

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPExceptionObj, QueryResult, ValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            label=label,
            user_id=user_id,
            data_id=data_id,
            start=start,
            end=end,
            limit=limit,
            step=step,
            direction=direction,
        )
    ).parsed
