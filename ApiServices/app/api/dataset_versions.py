# -------------------------------------------------------------------------------
# Engineering
# dataset_versions.py
# -------------------------------------------------------------------------------
"""APIs to manage dataset-versions"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Response, status
from fastapi.encoders import jsonable_encoder

import app.utils.azure as azure
from app.api.accounts import get_organization
from app.api.authentication import RoleChecker, get_current_user
from app.api.datasets import get_dataset
from app.api.internal_utils import cache_get_basic_info_organization
from app.data import operations as data_service
from app.log import log_message
from app.utils.background_couroutines import add_async_task
from app.utils.secrets import get_secret
from models.accounts import UserRole
from models.authentication import TokenData
from models.common import BasicObjectInfo, PyObjectId
from models.dataset_versions import (
    DatasetVersion_Db,
    DatasetVersionState,
    GetDatasetVersion_Out,
    GetDatasetVersionConnectionString_Out,
    GetMultipleDatasetVersion_Out,
    RegisterDatasetVersion_In,
    RegisterDatasetVersion_Out,
    UpdateDatasetVersion_In,
)
from models.datasets import DatasetState

DB_COLLECTION_DATASET_VERSIONS = "dataset-versions"

router = APIRouter()


########################################################################################################################
@router.post(
    path="/dataset-versions",
    description="Register new dataset-version",
    response_description="Dataset Version Id",
    response_model=RegisterDatasetVersion_Out,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
    operation_id="register_dataset_version",
)
async def register_dataset_version(
    response: Response,
    dataset_version_req: RegisterDatasetVersion_In = Body(description="Dataset Version information to register"),
    current_user: TokenData = Depends(get_current_user),
) -> RegisterDatasetVersion_Out:
    # Check if dataset version was already registered with the same name
    dataset_version_db = await data_service.find_one(
        DB_COLLECTION_DATASET_VERSIONS,
        {
            "name": dataset_version_req.name,
            "dataset_id": str(dataset_version_req.dataset_id),
            "organization_id": str(current_user.organization_id),
        },
    )
    # If the dataset version was already registered, return the dataset version id
    if dataset_version_db:
        response.status_code = status.HTTP_200_OK
        return RegisterDatasetVersion_Out(**dataset_version_db)  # type: ignore

    # Dataset organization and dataset-versions organization should be same
    dataset_db = await get_dataset(dataset_version_req.dataset_id, current_user)
    if dataset_db.organization.id != current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Dataset not found")

    # The dataset should be in active state
    if dataset_db.state != DatasetState.ACTIVE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Dataset is not active. Try again later")

    # Add the dataset to the database
    dataset_version_db = DatasetVersion_Db(
        **dataset_version_req.dict(),
        organization_id=current_user.organization_id,
        state=DatasetVersionState.CREATING_DIRECTORY,
    )
    await data_service.insert_one(DB_COLLECTION_DATASET_VERSIONS, jsonable_encoder(dataset_version_db))

    # Create a directory in the azure file share for the dataset version
    add_async_task(create_directory_in_file_share(dataset_version_db.dataset_id, dataset_version_db.id))

    message = f"[Register Dataset Version]: user_id:{current_user.id}, dataset_id: {dataset_version_req.dataset_id}, version: {dataset_version_db.id}"
    await log_message(message)

    return RegisterDatasetVersion_Out(**dataset_version_db.dict())


########################################################################################################################
@router.get(
    path="/dataset-versions",
    description="Get list of all the dataset-versions for the dataset",
    response_description="List of dataset-versions for the dataset",
    response_model=GetMultipleDatasetVersion_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    operation_id="get_all_dataset_versions",
)
async def get_all_dataset_versions(
    dataset_id: PyObjectId = Body(description="UUID of the dataset"),
    current_user: TokenData = Depends(get_current_user),
) -> GetMultipleDatasetVersion_Out:
    query = {"dataset_id": str(dataset_id)}
    dataset_versions = await data_service.find_by_query(DB_COLLECTION_DATASET_VERSIONS, query)

    response_list_of_dataset_version: List[GetDatasetVersion_Out] = []

    # Cache the organization information
    organization_cache = {}

    # Add the organization information to the dataset
    for dataset_version in dataset_versions:
        dataset_version = DatasetVersion_Db(**dataset_version)

        if dataset_version.organization_id not in organization_cache:
            organization_cache[dataset_version.organization_id] = await get_organization(
                organization_id=dataset_version.organization_id, current_user=current_user
            )

        response_dataset_version = GetDatasetVersion_Out(
            **dataset_version.dict(), organization=organization_cache[dataset_version.organization_id]
        )
        response_list_of_dataset_version.append(response_dataset_version)

    message = f"[Get All Dataset Version]: user_id:{current_user.id}, dataset_id:{dataset_id}"
    await log_message(message)

    return GetMultipleDatasetVersion_Out(dataset_versions=response_list_of_dataset_version)


########################################################################################################################
@router.get(
    path="/dataset-versions/{dataset_version_id}",
    description="Get the information about a dataset",
    response_model=GetDatasetVersion_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    operation_id="get_dataset_version",
)
async def get_dataset_version(
    dataset_version_id: PyObjectId = Path(description="UUID of the dataset version"),
    current_user: TokenData = Depends(get_current_user),
) -> GetDatasetVersion_Out:
    dataset_version = await data_service.find_one(DB_COLLECTION_DATASET_VERSIONS, {"_id": str(dataset_version_id)})
    if not dataset_version:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset version not found")
    dataset_version = DatasetVersion_Db(**dataset_version)  # type: ignore

    # Add the organization information to the dataset version
    _, organization = await cache_get_basic_info_organization({}, [dataset_version.organization_id], current_user)

    response_data_version = GetDatasetVersion_Out(
        **dataset_version.dict(), organization=BasicObjectInfo(id=organization[0].id, name=organization[0].name)
    )

    message = f"[Get Dataset Version]: user_id:{current_user.id}, dataset_id: {dataset_version.dataset_id}, version: {dataset_version_id}"
    await log_message(message)

    return response_data_version


########################################################################################################################
@router.get(
    path="/dataset-versions/{dataset_version_id}/connection-string",
    description="Get the write only connection string for the dataset version upload",
    response_model=GetDatasetVersionConnectionString_Out,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
    operation_id="get_dataset_version_connection_string",
)
async def get_dataset_version_connection_string(
    dataset_version_id: PyObjectId = Path(description="UUID of the dataset version"),
    current_user: TokenData = Depends(get_current_user),
) -> GetDatasetVersionConnectionString_Out:
    dataset_version = await data_service.find_one(
        DB_COLLECTION_DATASET_VERSIONS,
        {"_id": str(dataset_version_id), "organization_id": str(current_user.organization_id)},
    )
    if not dataset_version:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset version not found")
    dataset_version = DatasetVersion_Db(**dataset_version)  # type: ignore

    # Send the connection string only if the dataset version is not uploaded to prevent overwriting
    if dataset_version.state != DatasetVersionState.NOT_UPLOADED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Dataset version is already uploaded or in progress",
        )

    # Authenticate azure
    account_credentials = await azure.authenticate()
    dataset_version_file_name = f"dataset_{dataset_version.id}.zip"

    # Get the connection string for the dataset version which is valid for 30 minutes
    # This could be a long running operation
    connection_string = await azure.authentication_shared_access_signature(
        account_credentials=account_credentials,
        account_name=get_secret("azure_storage_account_name"),
        resource_group_name=get_secret("azure_storage_resource_group"),
        file_path=f"{dataset_version.id}/{dataset_version_file_name}",
        share_name=str(dataset_version.dataset_id),
        permission="cw",  # Create and write permission only
        expiry=datetime.utcnow() + timedelta(minutes=30),
    )

    url = f"https://{get_secret('azure_storage_account_name')}.file.core.windows.net/{dataset_version.dataset_id}/{dataset_version.id}"
    full_url = f"{url}/{dataset_version_file_name}?{connection_string.response}"

    message = f"[Get Dataset Version Connection String]: user_id:{current_user.id}, dataset_id: {dataset_version.dataset_id}. version: {dataset_version_id}"
    await log_message(message)

    return GetDatasetVersionConnectionString_Out(_id=dataset_version_id, connection_string=full_url)


########################################################################################################################
@router.put(
    path="/dataset-versions/{dataset_version_id}",
    description="Update dataset information",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="update_dataset_version",
)
async def update_dataset_version(
    dataset_version_id: PyObjectId = Path(description="UUID of the dataset version"),
    updated_dataset_version_info: UpdateDatasetVersion_In = Body(
        description="Object containing the information to be updated"
    ),
    current_user: TokenData = Depends(get_current_user),
):
    """
    Update the dataset version information

    :param dataset_version_id: The dataset version id
    :type dataset_version_id: PyObjectId
    :param updated_dataset_version_info: Object containing the information to be updated
    :type updated_dataset_version_info: UpdateDatasetVersion_In, optional
    :param current_user: inforamtion of the current user, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :raises HTTPException: Dataset not found
    :return: Response with no content
    :rtype: Response
    """
    # Dataset version must be part of same organization
    dataset_version_db = await data_service.find_one(
        DB_COLLECTION_DATASET_VERSIONS,
        {"_id": str(dataset_version_id), "organization_id": str(current_user.organization_id)},
    )
    if not dataset_version_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

    dataset_version_db = DatasetVersion_Db(**dataset_version_db)  # type: ignore

    if updated_dataset_version_info.description:
        dataset_version_db.description = updated_dataset_version_info.description

    if updated_dataset_version_info.state:
        dataset_version_db.state = updated_dataset_version_info.state

    await data_service.update_one(
        DB_COLLECTION_DATASET_VERSIONS,
        {"_id": str(dataset_version_id)},
        {"$set": jsonable_encoder(dataset_version_db)},
    )

    message = f"[Updata Dataset Version]: user_id:{current_user.id}, dataset_id: {dataset_version_db.dataset_id}, version: {dataset_version_id}"
    await log_message(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################################################################################################################
@router.delete(
    path="/dataset-versions/{dataset_version_id}",
    description="Disable a dataset version",
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN]))],
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="soft_delete_dataset_version",
)
async def soft_delete_dataset_version(
    dataset_version_id: PyObjectId = Path(description="UUID of the dataset version"),
    current_user: TokenData = Depends(get_current_user),
):
    # Dataset must be part of same organization
    dataset_version_db = await data_service.find_one(DB_COLLECTION_DATASET_VERSIONS, {"_id": str(dataset_version_id)})
    if not dataset_version_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
    dataset_version_db = DatasetVersion_Db(**dataset_version_db)  # type: ignore

    if dataset_version_db.organization_id != current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    # Disable the dataset
    dataset_version_db.state = DatasetVersionState.INACTIVE
    await data_service.update_one(
        DB_COLLECTION_DATASET_VERSIONS,
        {"_id": str(dataset_version_id)},
        {"$set": jsonable_encoder(dataset_version_db)},
    )

    message = f"[Soft Delete Dataset Version]: user_id:{current_user.id}, dataset_id: {dataset_version_db.dataset_id}, version: {dataset_version_id}"
    await log_message(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################################################################################################################
async def create_directory_in_file_share(dataset_id: PyObjectId, dataset_version_id: PyObjectId):
    """
    Create a directory in the Azure file share

    :param dataset_id: Dataset id
    :type dataset_id: PyObjectId
    :param dataset_version_id: Dataset version id
    :type dataset_version_id: PyObjectId
    """
    try:
        account_credentials = await azure.authenticate()

        # Get the connection string for the storage account
        connection_string_response = await azure.get_storage_account_connection_string(
            account_credentials=account_credentials,
            resource_group_name=get_secret("azure_storage_resource_group"),
            account_name=get_secret("azure_storage_account_name"),
        )
        if connection_string_response.status != "Success":
            raise Exception(connection_string_response.note)

        # Create the directory in the file share
        create_response = await azure.file_share_create_directory(
            connection_string=connection_string_response.response,
            file_share_name=str(dataset_id),
            directory_name=str(dataset_version_id),
        )
        if create_response.status != "Success":
            raise Exception(create_response.note)

        await data_service.update_one(
            DB_COLLECTION_DATASET_VERSIONS,
            {"_id": str(dataset_version_id)},
            {"$set": {"state": "NOT_UPLOADED"}},
        )

    except Exception as exception:
        await data_service.update_one(
            DB_COLLECTION_DATASET_VERSIONS,
            {"_id": str(dataset_id)},
            {"$set": {"state": "ERROR", "note": str(exception)}},
        )
