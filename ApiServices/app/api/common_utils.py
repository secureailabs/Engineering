# -------------------------------------------------------------------------------
# Engineering
# common_utils.py
# -------------------------------------------------------------------------------
"""SAIL internal util API functions"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
from app.data import operations as data_service
from fastapi import APIRouter, HTTPException, Response, status

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
