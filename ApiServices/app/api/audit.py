# -------------------------------------------------------------------------------
# Engineering
# audit.py
# -------------------------------------------------------------------------------
"""APIs to query audit logs"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

import asyncio
import functools
from typing import Optional, Union

import requests
from app.api.authentication import get_current_user
from app.api.data_federations_provisions import \
    get_all_data_federation_provision_info
from app.api.datasets import get_all_datasets
from app.utils.secrets import get_secret
from fastapi import APIRouter, Depends, HTTPException, status
from models.accounts import UserRole
from models.audit import QueryResult
from models.authentication import TokenData
from models.common import PyObjectId
from pydantic import Field, StrictStr

router = APIRouter()

audit_server_ip = get_secret("audit_service_ip")
audit_server_endpoint = f"http://{audit_server_ip}:3100/loki/api/v1/query_range"
print(audit_server_endpoint)


########################################################################################################################
@router.get(
    path="/audit/",
    description="query by logQL",
    response_description="audit log by stream",
    response_model=QueryResult,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
)
async def audit_incidents_query(
    label: StrictStr,
    userID: Optional[StrictStr] = None,
    dataID: Optional[StrictStr] = None,
    start: Optional[Union[int, float]] = None,
    end: Optional[Union[int, float]] = None,
    limit: Optional[int] = None,
    step: Optional[StrictStr] = None,
    direction: Optional[StrictStr] = None,
    current_user: TokenData = Depends(get_current_user),
):
    """
    perform a audit query

    :param query: query input
    :type query: QueryInput
    :param current_user: the user who perform the query, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :return: response body
    :rtype: json(dict)
    """
    query_raw = locals()
    query = {}
    query_raw.pop("current_user")
    for key in query_raw:
        if query_raw[key] is not None:
            query[key] = query_raw[key]

    label = query.pop("label")
    response = {}

    query_str = f'{{job="{label}"}}'
    '{job="user_activity"}'
    query["query"] = query_str

    if "userID" in query:
        userID = query.pop("userID")
        query_str = f'{query_str} |= `{str(userID)}`'
        query["query"] = query_str
        if label == "computation":
            response = await query_computation_byUserID(query, current_user)

    elif "dataID" in query:
        dataID = query.pop("dataID")
        query_str = f'{query_str} |= `{str(dataID)}`'
        query["query"] = query_str
        if label == "computation":
            response = await query_compuation_by_dataID(dataID, query, current_user)

    if label == "user_activity":
        response = await query_user_activity(query, current_user)

    return QueryResult(**response.json())


# #######################################################################################################################
async def query_computation_byUserID(
    query: dict,
    current_user: TokenData,
):
    """
    perform a query on scn computation activities

    :param query: query body
    :type query: dict
    :param current_user: the user who perform the query
    :type current_user: TokenData
    :return: response
    :rtype: dict(json)
    """

    response = {}
    # the user is SAIL tech support, no restriction
    if current_user.role == UserRole.ADMIN:
        response = await audit_query(query)

    # the user is research org admin, can only get info related to the VMs belongs to the org.
    elif current_user == UserRole.ORGANIZATION_ADMIN:

        provision_db = get_all_data_federation_provision_info(current_user)
        provision_db = provision_db.data_federation_provisions

        provision_VMs = []
        for provision in provision_db:
            provision_VMs.extend(provision.secure_computation_nodes_id)

        if len(provision_VMs) != 0:
            scn_ids = ""
            for scn_id in provision_VMs:
                scn_ids += scn_id
                scn_ids += "|"
            scn_ids = scn_ids[:-1]
            query["query"] = f'{query["query"]} |= `{str(scn_ids)}`'
        response = await audit_query(query)

    # the user is the data owner admin, can only get info about the data they own.
    elif current_user == UserRole.DATASET_ADMIN:

        datasets = await get_all_datasets(current_user)
        datasets = datasets.datasets

        if len(datasets) != 0:
            dataset_ids = ""
            for data in datasets:
                dataset_ids += data.id
                dataset_ids += "|"
            dataset_ids = dataset_ids[:-1]
            query["query"] = f'{query["query"]} |= `{str(dataset_ids)}`'
        response = await audit_query(query)

    # for other user identity, this is forbidden
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    return response


########################################################################################################################

async def query_compuation_by_dataID(
    dataset_id: PyObjectId,
    query: dict,
    current_user: TokenData,
):
    """
    query scn computation activities by dataID

    :param dataset_id: dataset id
    :type dataset_id: PyObjectId
    :param query: query body
    :type query: dict
    :param current_user: the user who perform the operation, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :return: response
    :rtype: json(dict)
    """

    response = {}
    # the user is SAIL tech support, no restriction
    if current_user.role == UserRole.ADMIN:
        response = await audit_query(query)

    # the user is research org admin, can only get info about data and nodes owned by the org.
    # check if data belongs to org
    elif current_user == UserRole.ORGANIZATION_ADMIN:
        data_ids = await get_dataset_from_user_node(current_user)
        if dataset_id in data_ids:
            response = await audit_query(query)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    # the user is the data owner admin, can only get info about the data they own.
    # check if data belongs to owner
    elif current_user == UserRole.DATASET_ADMIN:
        ###
        data_id = await get_all_datasets(current_user)
        data_id = data_id.datasets
        if len(data_id) == 0:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
        else:
            response = await audit_query(query)

    # for other user identity, this is forbidden
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    return QueryResult(**response.json())


########################################################################################################################
async def get_dataset_from_user_node(
    current_user: TokenData,
):
    """
    get dataset associated with an particular node

    :param current_user: the user who perform the query
    :type current_user: TokenData
    :return: data ids on the node
    :rtype: set
    """
    event_loop = asyncio.get_event_loop()
    nodes_info = await event_loop.run_in_executor(None, requests.get, current_user)

    data_busket = set()
    for node in nodes_info:
        for data in node["datasets"]:
            data_busket.update(data.id)

    return data_busket


########################################################################################################################
async def query_user_activity(
    query: dict,
    current_user: TokenData,
):
    """
    query for activities realted to api services

    :param query: query body
    :type query: dict
    :param current_user: the user who perform the query
    :type current_user: TokenData
    :return: response data
    :rtype: dict(json)
    """

    # the user is SAIL tech support, no restriction
    if current_user.role == UserRole.ADMIN:
        response = await audit_query(query)
    # for other user identity, this is forbidden
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    return response


########################################################################################################################
async def audit_query(
    query: dict,
):
    """
    send a query content to audit server, they possible query fields are:

    query: The LogQL query to perform
    limit: The max number of entries to return. It defaults to 100. Only applies to query types which produce a stream(log lines) response.
    start: The start time for the query as a nanosecond Unix epoch or another supported format. Defaults to one hour ago.
    end: The end time for the query as a nanosecond Unix epoch or another supported format. Defaults to now.
    direction: Determines the sort order of logs. Supported values are forward or backward. Defaults to backward.

    :param query: query content
    :type query: dict
    :return: response
    :rtype: dict
    """
    event_loop = asyncio.get_event_loop()

    response = await event_loop.run_in_executor(
        None,
        functools.partial(requests.get, audit_server_endpoint, params=query),
    )
    return response
