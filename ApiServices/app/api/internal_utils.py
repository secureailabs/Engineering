# -------------------------------------------------------------------------------
# Engineering
# internal_utils.py
# -------------------------------------------------------------------------------
"""SAIL internal util API functionses"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
from typing import Dict, List

from app.api.accounts import get_organization
from app.api.datasets import get_dataset
from app.data import operations as data_service
from fastapi import APIRouter, HTTPException, Response, status
from models.accounts import GetOrganizations_Out
from models.authentication import TokenData
from models.common import BasicObjectInfo, PyObjectId
from models.datasets import GetDataset_Out

router = APIRouter()


########################################################################################################################
@router.delete(
    path="/database", description="Drop the database", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def register_dataset():
    try:
        await data_service.drop()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
async def cache_get_basic_info_organization(
    organization_cache: Dict[PyObjectId, GetOrganizations_Out],
    organization_id_list: List[PyObjectId],
    current_user: TokenData,
):
    response_basic_info_list: List[GetOrganizations_Out] = []
    for organization_id in organization_id_list:
        if organization_id not in organization_cache:
            organization_cache[organization_id] = await get_organization(
                organization_id=organization_id, current_user=current_user
            )
            response_basic_info_list.append(organization_cache[organization_id])

    return (organization_cache, response_basic_info_list)


########################################################################################################################
async def cache_get_basic_info_datasets(
    datasets_cache: Dict[PyObjectId, GetDataset_Out],
    datasets_id_list: List[PyObjectId],
    current_user: TokenData,
):
    response_basic_info_list: List[GetDataset_Out] = []
    for datasets_id in datasets_id_list:
        if datasets_id not in datasets_cache:
            datasets_cache[datasets_id] = await get_dataset(dataset_id=datasets_id, current_user=current_user)
            response_basic_info_list.append(datasets_cache[datasets_id])

    return (datasets_cache, response_basic_info_list)
