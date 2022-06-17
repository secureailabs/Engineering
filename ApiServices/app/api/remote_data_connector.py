########################################################################################################################
# -------------------------------------------------------------------------------
# Engineering
# remote_data_connector.py
# -------------------------------------------------------------------------------
"""Temporary APIs to server remote data connector"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
from ipaddress import IPv4Address
from typing import List

from app.api.authentication import get_current_user
from app.data import operations as data_service
from fastapi import APIRouter, Body, Depends, HTTPException, status
from models.authentication import TokenData
from models.common import PyObjectId, SailBaseModel
from pydantic import Field

DB_COLLECTION_SECURE_COMPUTATION_NODE = "secure-computation-node"

router = APIRouter()


class GetWaitingSecureComputationNode_In(SailBaseModel):
    datasets: List[PyObjectId] = Field(...)


class VmUploadInfo(SailBaseModel):
    ipaddress: IPv4Address = Field(...)
    dataset_id: PyObjectId = Field(...)


class GetWaitingSecureComputationNode_Out(SailBaseModel):
    secure_computation_nodes: List[VmUploadInfo] = Field(...)


########################################################################################################################
@router.post(
    path="/remote-data-connectors/",
    description="Get list of all the secure_computation_node waiting for data",
    response_description="List of SCNs",
    response_model=GetWaitingSecureComputationNode_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_secure_computation_nodes_waiting_for_data(
    current_user: TokenData = Depends(get_current_user),
    datasets_with_remote_data_connector: GetWaitingSecureComputationNode_In = Body(...),
):
    try:
        response_secure_computation_nodes: List[VmUploadInfo] = []
        for dataset in datasets_with_remote_data_connector.datasets:
            query = {"dataset_id": str(dataset), "state": "WAITING_FOR_DATA"}
            secure_computation_nodes = await data_service.find_by_query(DB_COLLECTION_SECURE_COMPUTATION_NODE, query)
            for secure_computation_node in secure_computation_nodes:
                secure_computation_node = VmUploadInfo(**secure_computation_node)
                response_secure_computation_nodes.append(secure_computation_node)

        return GetWaitingSecureComputationNode_Out(secure_computation_nodes=response_secure_computation_nodes)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception
