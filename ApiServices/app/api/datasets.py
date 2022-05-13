########################################################################################################################
# @author Prawal Gangwar
# @brief APIs to manage datasets
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
########################################################################################################################

from typing import List

from app.api.authentication import RoleChecker, get_current_user
from app.data import operations as data_service
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from models.accounts import UserRole
from models.authentication import TokenData
from models.common import PyObjectId
from models.datasets import (
    Dataset_Db,
    DatasetState,
    GetDataset_Out,
    GetMultipleDataset_Out,
    RegisterDataset_In,
    RegisterDataset_Out,
    UpdateDataset_In,
)

########################################################################################################################
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
    dataset_req: RegisterDataset_In = Body(...), current_user: TokenData = Depends(get_current_user)
):
    try:
        # Check if the dataset is already registered
        dataset_db = await data_service.find_one(DB_COLLECTION_DATASETS, {"_id": str(dataset_req.id)})
        if dataset_db is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Dataset already registered")

        # Add the dataset to the database
        dataset_db = Dataset_Db(
            **dataset_req.dict(), organization_id=current_user.organization_id, state=DatasetState.ACTIVE
        )
        await data_service.insert_one(DB_COLLECTION_DATASETS, jsonable_encoder(dataset_db))

        return dataset_db
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.get(
    path="/datasets",
    description="Get list of all the datasets",
    response_description="List of datasets",
    response_model=GetMultipleDataset_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_all_datasets(current_user: TokenData = Depends(get_current_user)):
    try:
        datasets = await data_service.find_all(DB_COLLECTION_DATASETS)
        return GetMultipleDataset_Out(datasets=datasets)
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
        dataset = await data_service.find_one(DB_COLLECTION_DATASETS, {"_id": str(dataset_id)})
        if dataset is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
        return dataset
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


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
        if dataset_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

        dataset_db = Dataset_Db(**dataset_db)
        if dataset_db.organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        # TODO: Prawal find better way to update the dataset
        if updated_dataset_info.description is not None:
            dataset_db.description = updated_dataset_info.description

        if updated_dataset_info.name is not None:
            dataset_db.name = updated_dataset_info.name

        if updated_dataset_info.version is not None:
            dataset_db.version = updated_dataset_info.version

        if updated_dataset_info.keywords is not None:
            dataset_db.keywords = updated_dataset_info.keywords

        await data_service.update_one(
            DB_COLLECTION_DATASETS, {"_id": str(dataset_id)}, {"$set": jsonable_encoder(dataset_db)}
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
        if dataset_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

        dataset_db = Dataset_Db(**dataset_db)
        if dataset_db.organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        # Disable the dataset
        dataset_db.state = DatasetState.INACTIVE
        await data_service.update_one(
            DB_COLLECTION_DATASETS, {"_id": str(dataset_id)}, {"$set": jsonable_encoder(dataset_db)}
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception
