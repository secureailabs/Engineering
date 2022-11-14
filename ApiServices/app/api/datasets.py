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
from base64 import b64encode
import os

import app.utils.azure as azure
from app.api.accounts import get_organization
from app.api.authentication import RoleChecker, get_current_user
from app.data import operations as data_service
from app.data import sync_operations as sync_data_service
from app.log import log_message
from app.utils.secrets import get_secret
from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from models.accounts import UserRole
from models.authentication import TokenData
from models.common import BasicObjectInfo, PyObjectId, KeyVaultObject
from models.datasets import (
    Dataset_Db,
    DatasetState,
    GetDataset_Out,
    GetMultipleDataset_Out,
    RegisterDataset_In,
    RegisterDataset_Out,
    UpdateDataset_In,
    DatasetEncryptionKey_Out,
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
    response: Response,
    background_tasks: BackgroundTasks,
    dataset_req: RegisterDataset_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
) -> RegisterDataset_Out:
    """
    Register new dataset

    :param response: Response object
    :type response: Response
    :param background_tasks: Background tasks object to run tasks in the background
    :type background_tasks: BackgroundTasks
    :param dataset_req: information required to register a dataset, defaults to Body(...)
    :type dataset_req: RegisterDataset_In, optional
    :param current_user: information of current authenticated user, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :return: Dataset Id
    :rtype: RegisterDataset_Out
    """
    # Check if there is an existing dataset with the same name
    existing_dataset = await data_service.find_one(
        DB_COLLECTION_DATASETS, {"name": dataset_req.name, "organization_id": str(current_user.organization_id)}
    )
    # If there is an existing dataset with the same name, return the existing dataset ID
    if existing_dataset:
        dataset_db = Dataset_Db(**existing_dataset)
        response.status_code = status.HTTP_200_OK
        return RegisterDataset_Out(_id=dataset_db.id)

    # Add the dataset to the database
    dataset_db = Dataset_Db(
        **dataset_req.dict(), organization_id=current_user.organization_id, state=DatasetState.CREATING_STORAGE
    )
    await data_service.insert_one(DB_COLLECTION_DATASETS, jsonable_encoder(dataset_db))

    # Create a file share for the dataset
    background_tasks.add_task(create_azure_file_share, dataset_db.id)

    message = f"[Register Dataset]: user_id:{current_user.id}, dataset_id: {dataset_db.id}"
    await log_message(message)

    return RegisterDataset_Out(**dataset_db.dict())


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
    datasets = await data_service.find_by_query(
        DB_COLLECTION_DATASETS, {"organization_id": str(current_user.organization_id)}
    )

    # Add the organization information to the dataset
    organization = await get_organization(current_user.organization_id, current_user)

    response_list_of_datasets: List[GetDataset_Out] = []
    datasets_ids = []
    # Add the organization information to the dataset
    for dataset in datasets:
        dataset = Dataset_Db(**dataset)
        datasets_ids.append(dataset.id)
        response_dataset = GetDataset_Out(**dataset.dict(), organization=BasicObjectInfo(**organization.dict()))
        response_list_of_datasets.append(response_dataset)

    message = f"[Get All Datasets]: user_id:{current_user.id}, datasets_ids: {datasets_ids}"
    await log_message(message)

    return GetMultipleDataset_Out(datasets=response_list_of_datasets)


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
    dataset = await get_dataset_internal(dataset_id, current_user)
    organization_info = await get_organization(organization_id=dataset.organization_id, current_user=current_user)

    message = f"[Get Dataset]: user_id:{current_user.id}"
    await log_message(message)

    return GetDataset_Out(**dataset.dict(), organization=BasicObjectInfo(**organization_info.dict()))


async def get_dataset_internal(
    dataset_id: PyObjectId, current_user: TokenData = Depends(get_current_user)
) -> Dataset_Db:
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
    # Dataset must be part of same organization
    dataset_db = await data_service.find_one(DB_COLLECTION_DATASETS, {"_id": str(dataset_id)})
    if not dataset_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

    dataset_db = Dataset_Db(**dataset_db)
    if dataset_db.organization_id != current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    if updated_dataset_info.description:
        dataset_db.description = updated_dataset_info.description

    if updated_dataset_info.name:
        dataset_db.name = updated_dataset_info.name

    if updated_dataset_info.tag:
        dataset_db.tag = updated_dataset_info.tag

    await data_service.update_one(
        DB_COLLECTION_DATASETS,
        {"_id": str(dataset_id)},
        {"$set": jsonable_encoder(dataset_db)},
    )

    message = f"[Update Dataset]: user_id:{current_user.id}, dataset_id: {dataset_id}"
    await log_message(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################################################################################################################
@router.delete(
    path="/datasets/{dataset_id}",
    description="Disable the dataset",
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN]))],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def soft_delete_dataset(dataset_id: PyObjectId, current_user: TokenData = Depends(get_current_user)):
    # Dataset must be part of same organization
    dataset_db = await data_service.find_one(DB_COLLECTION_DATASETS, {"_id": str(dataset_id)})
    if not dataset_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

    dataset_db = Dataset_Db(**dataset_db)
    if dataset_db.organization_id != current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    # Disable the dataset
    dataset_db.state = DatasetState.INACTIVE
    await data_service.update_one(
        DB_COLLECTION_DATASETS,
        {"_id": str(dataset_id)},
        {"$set": jsonable_encoder(dataset_db)},
    )

    message = f"[Soft Delete Dataset]: user_id:{current_user.id}, dataset_id: {dataset_id}"
    await log_message(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def get_datset_encryption_key(
    dataset_id: PyObjectId, wrapping_key: KeyVaultObject, create_if_doesnt_exit: bool, current_user: TokenData
) -> DatasetEncryptionKey_Out:
    """
    Get the dataset encryption key to the database, if it does not exist, create it

    :param dataset_id: The dataset id
    :type dataset_id: PyObjectId
    :param rsa_key_name: The name of the wrapping RSA key
    :type rsa_key_name: str
    :param rsa_key_version: The version of the wrapping RSA key
    :type rsa_key_version: str
    :param current_user: The current user
    :type current_user: TokenData
    :return: base64 encoded dataset encryption key
    :rtype: DatasetEncryptionKey_Out
    """
    # Dataset organization and currnet user organization should be same
    dataset_db = await get_dataset_internal(dataset_id, current_user)

    # We generate a key if none has been assigned to this dataset, otherwise we unwrap the key
    # that was used to encrypt the DS
    if dataset_db.encryption_key is None:
        if not create_if_doesnt_exit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset encryption key not found")

        # Generate a new key. TODO: could be done in keyvault
        aes_key = os.urandom(32)

        wrapped_key_secret = azure.wrap_aes_key(
            aes_key=aes_key,
            wrapping_key=wrapping_key,
        )

        # Add the key information to the database
        dataset_db.encryption_key = wrapped_key_secret
        await data_service.update_one(
            DB_COLLECTION_DATASETS,
            {"_id": str(dataset_id)},
            {"$set": jsonable_encoder(dataset_db)},
        )
    else:
        wrapped_key_secret = dataset_db.encryption_key
        aes_key = azure.unwrap_aes_with_rsa_key(wrapped_aes_key=wrapped_key_secret, wrapping_key=wrapping_key)

    return DatasetEncryptionKey_Out(dataset_key=b64encode(aes_key).decode("ascii"))


def create_azure_file_share(dataset_id: PyObjectId):
    """
    Create a file share in Azure

    :param dataset_id: Dataset ID
    :type dataset_id: PyObjectId
    :raises Exception: failed to create file share
    """
    try:
        account_credentials = azure.authenticate()

        create_response = azure.create_file_share(
            account_credentials,
            get_secret("azure_storage_resource_group"),
            get_secret("azure_storage_account_name"),
            str(dataset_id),
        )
        if create_response.status != "Success":
            raise Exception(create_response.note)

        # Mark the dataset as active
        sync_data_service.update_one(DB_COLLECTION_DATASETS, {"_id": str(dataset_id)}, {"$set": {"state": "ACTIVE"}})

    except Exception as exception:
        sync_data_service.update_one(
            DB_COLLECTION_DATASETS, {"_id": str(dataset_id)}, {"$set": {"state": "ERROR", "note": str(exception)}}
        )
