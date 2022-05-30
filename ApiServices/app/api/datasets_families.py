########################################################################################################################
# @author Prawal Gangwar
# @brief APIs to manage dataset families
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
########################################################################################################################

from app.api.accounts import get_organization
from app.api.authentication import RoleChecker, get_current_user
from app.data import operations as data_service
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from models.accounts import UserRole
from models.authentication import TokenData
from models.common import PyObjectId
from models.datasets_families import (
    DatasetFamily_Db,
    DatasetFamilyState,
    GetDatasetFamily_Out,
    GetMultipleDatasetFamily_Out,
    RegisterDatasetFamily_In,
    RegisterDatasetFamily_Out,
    UpdateDatasetFamily_In,
)

DB_COLLECTION_DATASET_FAMILIES = "dataset-families"

router = APIRouter()


########################################################################################################################
@router.post(
    path="/dataset-families",
    description="Register new dataset family",
    response_description="DatasetFamily Id",
    response_model=RegisterDatasetFamily_Out,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
)
async def register_dataset_family(
    dataset_family_req: RegisterDatasetFamily_In = Body(...), current_user: TokenData = Depends(get_current_user)
):
    try:
        # Add the dataset family to the database
        dataset_family_db = DatasetFamily_Db(
            **dataset_family_req.dict(), organization_id=current_user.organization_id, state=DatasetFamilyState.ACTIVE
        )
        await data_service.insert_one(DB_COLLECTION_DATASET_FAMILIES, jsonable_encoder(dataset_family_db))

        return dataset_family_db
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.get(
    path="/dataset-families",
    description="Get list of all the dataset families",
    response_description="List of dataset families",
    response_model=GetMultipleDatasetFamily_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_all_dataset_families(current_user: TokenData = Depends(get_current_user)):
    try:
        dataset_families = await data_service.find_all(DB_COLLECTION_DATASET_FAMILIES)

        # Cache the organization information
        organization_cache = {}
        # Add the organization information to the dataset family
        for dataset_family in dataset_families:
            if dataset_family["organization_id"] not in organization_cache:
                organization_cache[dataset_family["organization_id"]] = await get_organization(
                    organization_id=dataset_family["organization_id"], current_user=current_user
                )
            dataset_family["organization"] = organization_cache[dataset_family["organization_id"]]
            dataset_family.pop("organization_id")

        return GetMultipleDatasetFamily_Out(dataset_families=dataset_families)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.get(
    path="/dataset-families/{dataset_family_id}",
    description="Get the information about a dataset family",
    response_model=GetDatasetFamily_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_dataset_family(dataset_family_id: PyObjectId, current_user: TokenData = Depends(get_current_user)):
    try:
        dataset_family = await data_service.find_one(DB_COLLECTION_DATASET_FAMILIES, {"_id": str(dataset_family_id)})
        if not dataset_family:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DatasetFamily not found")

        # Add the organization information to the dataset
        organization_info = await get_organization(
            organization_id=dataset_family["organization_id"], current_user=current_user
        )
        dataset_family["organization"] = organization_info
        dataset_family.pop("organization_id")

        return dataset_family
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.put(
    path="/dataset-families/{dataset_family_id}",
    description="Update dataset information",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_dataset_family(
    dataset_family_id: PyObjectId,
    updated_dataset_family_info: UpdateDatasetFamily_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
):
    try:
        # DatasetFamily must be part of same organization
        dataset_family_db = await data_service.find_one(DB_COLLECTION_DATASET_FAMILIES, {"_id": str(dataset_family_id)})
        if not dataset_family_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DatasetFamily not found")

        dataset_family_db = DatasetFamily_Db(**dataset_family_db)
        if dataset_family_db.organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        # TODO: Prawal find better way to update the dataset
        if updated_dataset_family_info.description:
            dataset_family_db.description = updated_dataset_family_info.description

        if updated_dataset_family_info.name:
            dataset_family_db.name = updated_dataset_family_info.name

        if updated_dataset_family_info.version:
            dataset_family_db.version = updated_dataset_family_info.version

        if updated_dataset_family_info.tag:
            dataset_family_db.tag = updated_dataset_family_info.tag

        await data_service.update_one(
            DB_COLLECTION_DATASET_FAMILIES,
            {"_id": str(dataset_family_id)},
            {"$set": jsonable_encoder(dataset_family_db)},
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.delete(
    path="/dataset-families/{dataset_family_id}",
    description="Disable the dataset",
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN]))],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def soft_delete_dataset_family(
    dataset_family_id: PyObjectId, current_user: TokenData = Depends(get_current_user)
):
    try:
        # DatasetFamily must be part of same organization
        dataset_family_db = await data_service.find_one(DB_COLLECTION_DATASET_FAMILIES, {"_id": str(dataset_family_id)})
        if not dataset_family_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DatasetFamily not found")

        dataset_family_db = DatasetFamily_Db(**dataset_family_db)
        if dataset_family_db.organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        # Disable the dataset
        dataset_family_db.state = DatasetFamilyState.INACTIVE
        await data_service.update_one(
            DB_COLLECTION_DATASET_FAMILIES,
            {"_id": str(dataset_family_id)},
            {"$set": jsonable_encoder(dataset_family_db)},
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception
