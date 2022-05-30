########################################################################################################################
# @author Prawal Gangwar
# @brief SAIL internal util API functions
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
########################################################################################################################

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
