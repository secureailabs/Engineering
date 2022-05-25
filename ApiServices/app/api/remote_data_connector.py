########################################################################################################################
# @author Prawal Gangwar
# @brief Temporary APIs to server remote data connector
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
########################################################################################################################

from typing import List

from app.api.authentication import get_current_user
from app.data import operations as data_service
from fastapi import APIRouter, Body, Depends, HTTPException, status
from models.authentication import TokenData
from models.common import PyObjectId, SailBaseModel
from models.secure_computation_nodes import GetMultipleSecureComputationNode_Out
from pydantic import Field

DB_COLLECTION_SECURE_COMPUTATION_NODE = "secure-computation-node"

router = APIRouter()


class GetWaitingSecureComputationNode_In(SailBaseModel):
    datasets: List[PyObjectId] = Field(...)


########################################################################################################################
@router.post(
    path="/remote-data-connectors/",
    description="Get list of all the secure_computation_node waiting for data",
    response_description="List of SCNs",
    response_model=GetMultipleSecureComputationNode_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_secure_computation_nodes_waiting_for_data(
    current_user: TokenData = Depends(get_current_user),
    datasets_with_remote_data_connector: GetWaitingSecureComputationNode_In = Body(...),
):
    try:
        response_secure_computation_nodes = []
        for dataset in datasets_with_remote_data_connector.datasets:
            query = {"dataset_id": str(dataset), "state": "WAITING_FOR_DATA"}
            secure_computation_nodes = await data_service.find_by_query(DB_COLLECTION_SECURE_COMPUTATION_NODE, query)
            for secure_computation_node in secure_computation_nodes:
                response_secure_computation_nodes.append(secure_computation_node)

        return GetMultipleSecureComputationNode_Out(secure_computation_nodes=response_secure_computation_nodes)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception
