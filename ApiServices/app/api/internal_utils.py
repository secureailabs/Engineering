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
from app.api.datasets_families import get_dataset_family
from app.data import operations as data_service
from fastapi import APIRouter, HTTPException, Response, status
from models.authentication import TokenData
from models.common import BasicObjectInfo, PyObjectId

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
    organization_cache: Dict[PyObjectId, BasicObjectInfo],
    organization_id_list: List[PyObjectId],
    current_user: TokenData,
):
    response_basic_info_list: List[BasicObjectInfo] = []
    for organization_id in organization_id_list:
        if organization_id not in organization_cache:
            organization_cache[organization_id] = await get_organization(
                organization_id=organization_id, current_user=current_user
            )
            response_basic_info_list.append(organization_cache[organization_id])

    return (organization_cache, response_basic_info_list)


########################################################################################################################
async def cache_get_basic_info_dataset_families(
    dataset_families_cache: Dict[PyObjectId, BasicObjectInfo],
    dataset_families_id_list: List[PyObjectId],
    current_user: TokenData,
):
    response_basic_info_list: List[BasicObjectInfo] = []
    for dataset_families_id in dataset_families_id_list:
        if dataset_families_id not in dataset_families_cache:
            dataset_families_cache[dataset_families_id] = await get_dataset_family(
                dataset_family_id=dataset_families_id, current_user=current_user
            )
            response_basic_info_list.append(dataset_families_cache[dataset_families_id])

    return (dataset_families_cache, response_basic_info_list)
