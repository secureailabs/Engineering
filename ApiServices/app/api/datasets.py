# -------------------------------------------------------------------------------
# Engineering
# datasets.py
# -------------------------------------------------------------------------------
"""APIs to manage datasets"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
from typing import List

import app.utils.azure as azure
from app.api.accounts import get_organization
from app.api.authentication import RoleChecker, get_current_user
from app.data import operations as data_service
from app.data import sync_operations as sync_data_service
from app.utils.secrets import get_secret
from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from models.accounts import UserRole
from models.authentication import TokenData
from models.common import BasicObjectInfo, PyObjectId
from models.datasets import (
    Dataset_Db,
    DatasetState,
    GetDataset_Out,
    GetMultipleDataset_Out,
    RegisterDataset_In,
    RegisterDataset_Out,
    UpdateDataset_In,
)

DB_COLLECTION_DATASETS = "datasets"

router = APIRouter()


########################################################################################################################
@router.post(
    path="/datasets",
    description="Register new dataset",
    response_description="Dataset Id",
    response_model=RegisterDataset_Out,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
)
async def register_dataset(
    background_tasks: BackgroundTasks,
    dataset_req: RegisterDataset_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
):
    try:
        # Add the dataset to the database
        dataset_db = Dataset_Db(
            **dataset_req.dict(), organization_id=current_user.organization_id, state=DatasetState.ACTIVE
        )
        await data_service.insert_one(DB_COLLECTION_DATASETS, jsonable_encoder(dataset_db))

        # Create a file share for the dataset
        background_tasks.add_task(create_azure_file_share, dataset_db.id)

        return dataset_db
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.get(
    path="/datasets",
    description="Get list of all the datasets for the current organization",
    response_description="List of datasets",
    response_model=GetMultipleDataset_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_all_datasets(current_user: TokenData = Depends(get_current_user)):
    try:
        datasets = await data_service.find_by_query(
            DB_COLLECTION_DATASETS, {"organization_id": str(current_user.organization_id)}
        )

        # Add the organization information to the dataset
        organization = await get_organization(current_user.organization_id, current_user)

        response_list_of_datasets: List[GetDataset_Out] = []
        # Add the organization information to the dataset
        for dataset in datasets:
            dataset = Dataset_Db(**dataset)
            response_dataset = GetDataset_Out(**dataset.dict(), organization=BasicObjectInfo(**organization.dict()))
            response_list_of_datasets.append(response_dataset)

        return GetMultipleDataset_Out(datasets=response_list_of_datasets)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.get(
    path="/datasets/{dataset_id}",
    description="Get the information about a dataset",
    response_model=GetDataset_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_dataset(dataset_id: PyObjectId, current_user: TokenData = Depends(get_current_user)):
    try:
        dataset = await get_dataset_internal(dataset_id, current_user)
        organization_info = await get_organization(organization_id=dataset.organization_id, current_user=current_user)

        return GetDataset_Out(**dataset.dict(), organization=BasicObjectInfo(**organization_info.dict()))
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


async def get_dataset_internal(dataset_id: PyObjectId, current_user: TokenData = Depends(get_current_user)):
    dataset = await data_service.find_one(DB_COLLECTION_DATASETS, {"_id": str(dataset_id)})
    if not dataset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

    # Add the organization information to the dataset
    dataset = Dataset_Db(**dataset)

    return dataset


########################################################################################################################
@router.put(
    path="/datasets/{dataset_id}",
    description="Update dataset information",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_dataset(
    dataset_id: PyObjectId,
    updated_dataset_info: UpdateDataset_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
):
    try:
        # Dataset must be part of same organization
        dataset_db = await data_service.find_one(DB_COLLECTION_DATASETS, {"_id": str(dataset_id)})
        if not dataset_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

        dataset_db = Dataset_Db(**dataset_db)  # type: ignore
        if dataset_db.organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        if updated_dataset_info.description:
            dataset_db.description = updated_dataset_info.description

        if updated_dataset_info.name:
            dataset_db.name = updated_dataset_info.name

        if updated_dataset_info.version:
            dataset_db.version = updated_dataset_info.version

        if updated_dataset_info.tag:
            dataset_db.tag = updated_dataset_info.tag

        await data_service.update_one(
            DB_COLLECTION_DATASETS,
            {"_id": str(dataset_id)},
            {"$set": jsonable_encoder(dataset_db)},
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.delete(
    path="/datasets/{dataset_id}",
    description="Disable the dataset",
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN]))],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def soft_delete_dataset(dataset_id: PyObjectId, current_user: TokenData = Depends(get_current_user)):
    try:
        # Dataset must be part of same organization
        dataset_db = await data_service.find_one(DB_COLLECTION_DATASETS, {"_id": str(dataset_id)})
        if not dataset_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

        dataset_db = Dataset_Db(**dataset_db)  # type: ignore
        if dataset_db.organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        # Disable the dataset
        dataset_db.state = DatasetState.INACTIVE
        await data_service.update_one(
            DB_COLLECTION_DATASETS,
            {"_id": str(dataset_id)},
            {"$set": jsonable_encoder(dataset_db)},
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


def create_azure_file_share(dataset_id: PyObjectId):
    """
    Create a file share in Azure

    :param dataset_id: Dataset ID
    :type dataset_id: PyObjectId
    :raises Exception: failed to create file share
    """
    try:
        account_credentials = azure.authenticate(
            get_secret("azure_client_id"),
            get_secret("azure_client_secret"),
            get_secret("azure_tenant_id"),
            get_secret("azure_subscription_id"),
        )

        create_response = azure.create_file_share(
            account_credentials,
            get_secret("azure_storage_resource_group"),
            get_secret("azure_storage_account_name"),
            str(dataset_id),
        )
        if create_response.status != "Success":
            raise Exception(create_response.note)
    except Exception as exception:
        sync_data_service.update_one(
            DB_COLLECTION_DATASETS, {"_id": str(dataset_id)}, {"$set": {"state": "ERROR", "note": str(exception)}}
        )
