# -------------------------------------------------------------------------------
# Engineering
# data_federations_provisions.py
# -------------------------------------------------------------------------------
"""APIs to manage data-federations-provisions"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

from typing import List

from app.api.authentication import get_current_user
from app.api.data_federations import get_data_federation
from app.api.dataset_versions import get_all_dataset_versions
from app.api.secure_computation_nodes import deprovision_secure_computation_nodes, register_secure_computation_node
from app.data import operations as data_service
from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from models.authentication import TokenData
from models.common import PyObjectId
from models.data_federations import (
    DataFederationProvision_Db,
    GetDataFederationProvision,
    GetMultipleDataFederationProvision_Out,
    RegisterDataFederationProvision_In,
    RegisterDataFederationProvision_Out,
)
from models.secure_computation_nodes import RegisterSecureComputationNode_In, SecureComputationNodeType

DB_COLLECTION_DATA_FEDERATIONS_PROVISIONS = "data-federation-provsions"

router = APIRouter()


########################################################################################################################
@router.post(
    path="/data-federations-provisions",
    description="Provision data federation SCNs",
    response_description="Data Federation Provision Id and list of SCNs",
    response_model=RegisterDataFederationProvision_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_201_CREATED,
)
async def provision_data_federation(
    background_tasks: BackgroundTasks,
    provision_req: RegisterDataFederationProvision_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
) -> RegisterDataFederationProvision_Out:
    """
    Provision data federation SCNs

    :param background_tasks: Background tasks
    :type background_tasks: BackgroundTasks
    :param provision_req: information required for provsioning, defaults to Body(...)
    :type provision_req: RegisterDataFederationProvision_In, optional
    :param current_user: current user information
    :type current_user: TokenData, optional
    :raises HTTPException: 404 if data federation not found
    :raises HTTPException: 403 if user is not authorized
    :return: Data Federation Provision Id and list of SCNs
    :rtype: RegisterDataFederationProvision_Out
    """
    try:
        # Current user organization must be one of the the data federation researcher
        data_federation_db = await get_data_federation(
            data_federation_id=provision_req.data_federation_id, current_user=current_user
        )
        if not data_federation_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Federation not found")

        # Researcher must be one of the data federation researchers
        if [
            organization
            for organization in data_federation_db.research_organizations
            if organization.id == current_user.organization_id
        ] is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Organization must be one of the the data federation researcher",
            )

        # Create a new provision object
        provision_db = DataFederationProvision_Db(
            data_federation_id=provision_req.data_federation_id,
            organization_id=current_user.organization_id,
            secure_computation_nodes_type=provision_req.secure_computation_nodes_type,
            secure_computation_nodes_id=[],
        )

        # Get the dataset versions for the data federation
        datasets = data_federation_db.datasets
        for dataset in datasets:
            # Get the dataset versions
            dataset_id = dataset.id
            response = await get_all_dataset_versions(dataset_id=dataset_id, current_user=current_user)

            # Get the latest version
            latest_version = response.dataset_versions[0].id

            # Provision the latest version
            register_scn_params = RegisterSecureComputationNode_In(
                data_federation_id=provision_req.data_federation_id,
                data_federation_provision_id=provision_db.id,
                dataset_id=dataset_id,
                dataset_version_id=latest_version,
                type=SecureComputationNodeType.Standard_D4s_v4,
            )

            # Provision the SCN and get the SCN id
            scn_provision_response = await register_secure_computation_node(
                background_tasks=background_tasks,
                secure_computation_node_req=register_scn_params,
                current_user=current_user,
            )

            provision_db.secure_computation_nodes_id.append(scn_provision_response.id)

        await data_service.insert_one(DB_COLLECTION_DATA_FEDERATIONS_PROVISIONS, jsonable_encoder(provision_db))

        return RegisterDataFederationProvision_Out(**provision_db.dict())
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.get(
    path="/data-federations-provsions/{provision_id}",
    description="Get data federation provision SCNs",
    response_description="Data Federation Provision information and list of SCNs",
    response_model=GetDataFederationProvision,
    status_code=status.HTTP_200_OK,
)
async def get_data_federation_provision_info(
    provision_id: PyObjectId,
    current_user: TokenData = Depends(get_current_user),
) -> GetDataFederationProvision:
    """
    Get data federation provision information

    :param provision_id: Data Federation Provision Id
    :type provision_id: PyObjectId
    :param current_user: current user information, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :raises HTTPException: 404 if data federation provision not found
    :return: Data Federation Provision information and list of SCNs
    :rtype: GetDataFederationProvision
    """
    try:
        # Get the data federation provision
        provision_db = await data_service.find_one(
            DB_COLLECTION_DATA_FEDERATIONS_PROVISIONS,
            {"_id": str(provision_id), "organization_id": str(current_user.organization_id)},
        )
        if not provision_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Federation Provision not found")

        return GetDataFederationProvision(**provision_db)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.get(
    path="/data-federations-provsions",
    description="Get all data federation provision SCNs",
    response_description="All Data Federation Provision information and list of SCNs for the current organization",
    response_model=GetMultipleDataFederationProvision_Out,
    status_code=status.HTTP_200_OK,
)
async def get_all_data_federation_provision_info(
    current_user: TokenData = Depends(get_current_user),
) -> GetMultipleDataFederationProvision_Out:
    """
    Get all data federation provision information

    :param provision_id: Data Federation Provision Id
    :type provision_id: PyObjectId
    :param current_user: current user information, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :raises HTTPException: 404 if data federation provision not found
    :return: Data Federation Provision information and list of SCNs
    :rtype: GetDataFederationProvision
    """
    try:
        # Get the data federation provision
        provision_db = await data_service.find_by_query(
            DB_COLLECTION_DATA_FEDERATIONS_PROVISIONS,
            {"organization_id": str(current_user.organization_id)},
        )

        response_list: List[GetDataFederationProvision] = []
        for provision in provision_db:
            response_list.append(GetDataFederationProvision(**provision))

        return GetMultipleDataFederationProvision_Out(data_federation_provisions=response_list)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.delete(
    path="/data-federations-provisions/{provision_id}",
    description="DeProvision data federation SCNs",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def deprovision_data_federation(
    background_tasks: BackgroundTasks,
    provision_id: PyObjectId,
    current_user: TokenData = Depends(get_current_user),
):
    """
    Deprovision data federation SCNs

    :param background_tasks: background tasks
    :type background_tasks: BackgroundTasks
    :param provision_id: Data Federation Provision Id
    :type provision_id: PyObjectId
    :param current_user: current user information, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :raises http_exception: 404 if data federation provision not found
    :return: None
    :rtype: Response
    """
    try:
        # Provision the SCN and get the SCN id
        await deprovision_secure_computation_nodes(
            background_tasks=background_tasks,
            data_federation_provision_id=provision_id,
            current_user=current_user,
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception
