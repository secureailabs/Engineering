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
from typing import List, Optional

from app.api.accounts import get_organization
from app.api.authentication import RoleChecker, get_current_user
from app.api.internal_utils import cache_get_basic_info_organization
from app.data import operations as data_service
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from models.accounts import UserRole
from models.authentication import TokenData
from models.common import PyObjectId
from models.dataset_versions import (
    DatasetVersion_Db,
    DatasetVersionState,
    GetDatasetVersion_Out,
    GetMultipleDatasetVersion_Out,
    RegisterDatasetVersion_In,
    RegisterDatasetVersion_Out,
    UpdateDatasetVersion_In,
)

DB_COLLECTION_DATASETS = "dataset-versions"

router = APIRouter()


########################################################################################################################
@router.post(
    path="/dataset-versions",
    description="Register new dataset-version",
    response_description="Dataset Version Id",
    response_model=RegisterDatasetVersion_Out,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
)
async def register_dataset_version(
    dataset_req: RegisterDatasetVersion_In = Body(...), current_user: TokenData = Depends(get_current_user)
) -> RegisterDatasetVersion_Out:
    try:
        # Check if the dataset is already registered
        dataset_version_db = await data_service.find_one(DB_COLLECTION_DATASETS, {"_id": str(dataset_req.id)})
        if dataset_version_db:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Dataset already registered")

        # Add the dataset to the database
        dataset_version_db = DatasetVersion_Db(
            **dataset_req.dict(), organization_id=current_user.organization_id, state=DatasetVersionState.ACTIVE
        )
        await data_service.insert_one(DB_COLLECTION_DATASETS, jsonable_encoder(dataset_version_db))

        return RegisterDatasetVersion_Out(**dataset_version_db.dict())
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.get(
    path="/dataset-versions",
    description="Get list of all the dataset-versions for the dataset",
    response_description="List of dataset-versions for the dataset",
    response_model=GetMultipleDatasetVersion_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_all_dataset_versions(
    dataset_id: PyObjectId,
    current_user: TokenData = Depends(get_current_user),
) -> GetMultipleDatasetVersion_Out:
    try:
        query = {"dataset_id": str(dataset_id)}
        dataset_versions = await data_service.find_by_query(DB_COLLECTION_DATASETS, query)

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

        return GetMultipleDatasetVersion_Out(dataset_versions=response_list_of_dataset_version)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.get(
    path="/dataset-versions/{dataset_version_id}",
    description="Get the information about a dataset",
    response_model=GetDatasetVersion_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_dataset_version(
    dataset_version_id: PyObjectId, current_user: TokenData = Depends(get_current_user)
) -> GetDatasetVersion_Out:
    try:
        dataset_version = await data_service.find_one(DB_COLLECTION_DATASETS, {"_id": str(dataset_version_id)})
        if not dataset_version:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset version not found")
        dataset_version = DatasetVersion_Db(**dataset_version)  # type: ignore

        # Add the organization information to the data federation
        _, organization = await cache_get_basic_info_organization({}, [dataset_version.organization_id], current_user)

        response_data_federation = GetDatasetVersion_Out(**dataset_version.dict(), organization=organization[0])

        return response_data_federation
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.put(
    path="/dataset-versions/{dataset_version_id}",
    description="Update dataset information",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_dataset_version(
    dataset_version_id: PyObjectId,
    updated_dataset_version_info: UpdateDatasetVersion_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
):
    try:
        # Dataset version must be part of same organization
        dataset_version_db = await data_service.find_one(DB_COLLECTION_DATASETS, {"_id": str(dataset_version_id)})
        if not dataset_version_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

        dataset_version_db = DatasetVersion_Db(**dataset_version_db)  # type: ignore
        if dataset_version_db.organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        if updated_dataset_version_info.description:
            dataset_version_db.description = updated_dataset_version_info.description

        if updated_dataset_version_info.name:
            dataset_version_db.name = updated_dataset_version_info.name

        if updated_dataset_version_info.version:
            dataset_version_db.version = updated_dataset_version_info.version

        if updated_dataset_version_info.keywords:
            dataset_version_db.keywords = updated_dataset_version_info.keywords

        await data_service.update_one(
            DB_COLLECTION_DATASETS, {"_id": str(dataset_version_id)}, {"$set": jsonable_encoder(dataset_version_db)}
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.delete(
    path="/dataset-versions/{dataset_version_id}",
    description="Disable a dataset version",
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN]))],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def soft_delete_dataset_version(
    dataset_version_id: PyObjectId, current_user: TokenData = Depends(get_current_user)
):
    try:
        # Dataset must be part of same organization
        dataset_version_db = await data_service.find_one(DB_COLLECTION_DATASETS, {"_id": str(dataset_version_id)})
        if not dataset_version_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
        dataset_version_db = DatasetVersion_Db(**dataset_version_db)  # type: ignore

        if dataset_version_db.organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        # Disable the dataset
        dataset_version_db.state = DatasetVersionState.INACTIVE
        await data_service.update_one(
            DB_COLLECTION_DATASETS, {"_id": str(dataset_version_id)}, {"$set": jsonable_encoder(dataset_version_db)}
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception
