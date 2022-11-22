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
import json

import requests
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.authentication import RoleChecker, get_current_user
from app.data import operations as data_service
from models.accounts import UserRole
from models.authentication import TokenData
from models.common import AuditIncident, PyObjectId

router = APIRouter()


endpoint = "/loki/api/v1/query_range"
config = {}
with open("InitializationVector.json", "r") as f:
    config = json.load(f)
audit_server_endpoint = f"{config['audit_server_ip']}{endpoint}:{config['audit_server_port']}"

# #######################################################################################################################
@router.post(
    path="/audit/activity/time/",
    description="query by a LogQL string",
    response_model=QueryResult,
    response_model_by_alias=False,
    status_code=status.HTTP_201_OK,
)
async def audit_query_activity_by_time(
    start: int,
    end: int,
    current_user: TokenData = Depends(get_current_user),
):
    query = {
        "query": f'{{job_name="user_activity"}}',
        "start": start,
        "end": end,
    }
    response = await query_user_activity(query, current_user)
    return response


# #######################################################################################################################
@router.post(
    path="/audit/computation/time/",
    description="query by a LogQL string",
    response_model=QueryResult,
    response_model_by_alias=False,
    status_code=status.HTTP_201_OK,
)
async def audit_query_computation_by_time(
    start: int,
    end: int,
    current_user: TokenData = Depends(get_current_user),
):

    query = {
        "query": f'{{job_name="user_activity"}}',
        "start": start,
        "end": end,
    }
    response = await query_computation(query, current_user)

    return response


# #######################################################################################################################
@router.post(
    path="/audit/activity/userID/",
    description="query by a LogQL string",
    response_model=QueryResult,
    response_model_by_alias=False,
    status_code=status.HTTP_201_OK,
)
async def audit_query_activity_by_userID(
    user_id: pyObjectId,
    start: int = 0,
    end: int = 100,
    current_user: TokenData = Depends(get_current_user),
):

    query = {
        "query": f'{{job_name="user_activity"}} |= {user_id}',
        "start": start,
        "end": end,
    }
    response = await query_user_activity(query, current_user)
    return response


# #######################################################################################################################
@router.post(
    path="/audit/computation/userID/",
    description="query by a LogQL string",
    response_model=QueryResult,
    response_model_by_alias=False,
    status_code=status.HTTP_201_OK,
)
async def audit_query_computation_by_userID(
    user_id: PyObjectId,
    start: int,
    end: int,
    current_user: TokenData = Depends(get_current_user),
):
    query = {
        "query": f'{{job_name="user_activity"}} |= `{user_id}`',
        "start": start,
        "end": end,
    }
    response = await query_computation(query, current_user)
    return response


async def query_computation(
    query: dict,
    current_user: TokenData,
):
    try:
        response = {}
        # the user is SAIL tech support, no restriction
        if current_user.role == UserRole.SAIL_ADMIN:
            response = await audit_query(query)

        # the user is research org admin, can only get info related to the VMs belongs to the org.
        elif current_user == UserRole.ADMIN:
            provision_db = await data_service.find_by_query(
                "data-federation-provsions",
                {"organization_id": str(current_user.organization_id)},
            )

            provision_VMs = []
            for provision in provision_db:
                provision_VMs.extend(provision.secure_computation_nodes_id)

            if len(provision_VMs) != 0:
                scn_ids = ""
                for scn_id in provision_VMs:
                    scn_ids += scn_id
                    scn_ids += "|"
                scn_ids = scn_ids[:-1]
                query["query"] = f'{query["query"]} |= `{scn_ids}`'
            response = await audit_query(query)

        # the user is the data owner admin, can only get info about the data they own.
        elif current_user == UserRole.DATASET_ADMIN:
            datasets = await data_service.find_by_query(
                "datasets", {"organization_id": str(current_user.organization_id)}
            )
            if len(datasets) != 0:
                dataset_ids = ""
                for data in datasets:
                    dataset_ids += data.id
                    dataset_ids += "|"
                dataset_ids = dataset_ids[:-1]
                query["query"] = f'{query["query"]} |= `{dataset_ids}`'
            response = await audit_query(query)

        # for other user identity, this is forbidden
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        return response

    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


# #######################################################################################################################
@router.post(
    path="/audit/computation/dataID/",
    description="query by a LogQL string",
    response_model=QueryResult,
    response_model_by_alias=False,
    status_code=status.HTTP_201_OK,
)
async def audit_query_compuation_by_dataID(
    dataset_id: PyObjectId,
    start: int = 0,
    end: int = 100,
    current_user: TokenData = Depends(get_current_user),
):
    try:
        query = {
            "query": f'{{job_name="computation"}} |= `{dataset_id}`',
            "start": start,
            "end": end,
        }

        response = {}
        # the user is SAIL tech support, no restriction
        if current_user.role == UserRole.SAIL_ADMIN:
            response = await audit_query(query)

        # the user is research org admin, can only get info about data and nodes owned by the org.
        # check if data belongs to org
        elif current_user == UserRole.ADMIN:
            data_ids = await get_dataset_from_user_node(current_user)
            if dataset_id in data_ids:
                response = await audit_query(query)
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        # the user is the data owner admin, can only get info about the data they own.
        # check if data belongs to owner
        elif current_user == UserRole.DATASET_ADMIN:
            data_id = await data_service.find_one("datasets", {"_id": str(dataset_id)})
            if not data_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
            else:
                response = await audit_query(query)

        # for other user identity, this is forbidden
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        return response

    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


async def get_dataset_from_user_node(
    current_user: TokenData,
):
    try:
        event_loop = asyncio.get_event_loop()
        nodes_info = await event_loop.run_in_executor(None, requests.get, current_user)

        data_busket = set()
        for node in nodes_info:
            for data in node["datasets"]:
                data_busket.update(data.id)

        return data_busket

    except Exception as exception:
        raise exception


# #######################################################################################################################
@router.post(
    path="/audit/activity/dataID/",
    description="query by a LogQL string",
    response_model=QueryResult,
    response_model_by_alias=False,
    status_code=status.HTTP_201_OK,
)
async def audit_query_activity_by_dataID(
    data_id: PyObjectId,
    start: int = 0,
    end: int = 100,
    current_user: TokenData = Depends(get_current_user),
):
    query = {
        "query": f'{{job_name="user_activity"}} |= `{data_id}`',
        "start": start,
        "end": end,
    }

    response = await query_user_activity(query, current_user)
    return response


# #######################################################################################################################
@router.post(
    path="/audit/",
    description="query by a LogQL string",
    response_model=QueryResult,
    response_model_by_alias=False,
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN]))],
    status_code=status.HTTP_201_OK,
)
async def audit_query_general(
    query: dict,
    current_user: TokenData = Depends(get_current_user),
):
    response = await query_user_activity(query, current_user)
    return response


async def query_user_activity(
    query: dict,
    current_user: TokenData,
):
    try:
        # the user is SAIL tech support, no restriction
        if current_user.role == UserRole.SAIL_ADMIN:
            response = await audit_query(dict)
        # for other user identity, this is forbidden
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
        return response

    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


# #######################################################################################################################
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
    try:
        event_loop = asyncio.get_event_loop()

        response = await event_loop.run_in_executor(None, requests.get, audit_server_endpoint, query)
        return response

    except Exception as exception:
        raise exception
