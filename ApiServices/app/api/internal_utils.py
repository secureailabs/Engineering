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

from fastapi import APIRouter, Response, status

from app.api.accounts import get_organization
from app.api.datasets import get_dataset
from app.data import operations as data_service
from models.authentication import TokenData
from models.common import BasicObjectInfo, PyObjectId

router = APIRouter()


########################################################################################################################
@router.delete(
    path="/database",
    description="Drop the database",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="drop_database",
)
async def register_dataset():
    await data_service.drop()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################################################################################################################
async def cache_get_basic_info_organization(
    organization_cache: Dict[PyObjectId, BasicObjectInfo],
    organization_id_list: List[PyObjectId],
    current_user: TokenData,
):
    response_basic_info_list: List[BasicObjectInfo] = []
    for organization_id in organization_id_list:
        if organization_id not in organization_cache:
            organization_basic_info = await get_organization(organization_id=organization_id, current_user=current_user)
            organization_cache[organization_id] = BasicObjectInfo(
                _id=organization_basic_info.id, name=organization_basic_info.name
            )
            response_basic_info_list.append(organization_cache[organization_id])

    return (organization_cache, response_basic_info_list)


########################################################################################################################
async def cache_get_basic_info_datasets(
    datasets_cache: Dict[PyObjectId, BasicObjectInfo],
    datasets_id_list: List[PyObjectId],
    current_user: TokenData,
):
    response_basic_info_list: List[BasicObjectInfo] = []
    for datasets_id in datasets_id_list:
        if datasets_id not in datasets_cache:
            dataset_basic_info = await get_dataset(dataset_id=datasets_id, current_user=current_user)
            datasets_cache[datasets_id] = BasicObjectInfo(_id=dataset_basic_info.id, name=dataset_basic_info.name)
            response_basic_info_list.append(datasets_cache[datasets_id])

    return (datasets_cache, response_basic_info_list)
