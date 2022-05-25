########################################################################################################################
# @author Prawal Gangwar
# @brief APIs to manage datasets
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
########################################################################################################################

from typing import List, Optional
from fastapi import APIRouter, Depends, Body, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from models.datasets import Dataset_Db
from app.api.datasets import get_dataset
from models.accounts import UserRole
from models.authentication import TokenData
from models.common import PyObjectId
from app.api.authentication import RoleChecker, get_current_user
from app.data import operations as data_service
from models.digital_contracts import (
    DigitalContract_Db,
    DigitalContractState,
    GetDigitalContract_Out,
    RegisterDigitalContract_In,
    RegisterDigitalContract_Out,
    UpdateDigitalContract_In,
)

########################################################################################################################
DB_COLLECTION_DIGITAL_CONTRACTS = "digital-contracts"

router = APIRouter()


########################################################################################################################
@router.post(
    path="/digital-contracts",
    description="Register new digital contract",
    response_description="Digital Contract Id",
    response_model=RegisterDigitalContract_Out,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
)
async def register_digital_contract(
    digital_contract_req: RegisterDigitalContract_In = Body(...), current_user: TokenData = Depends(get_current_user)
):
    try:
        # Check of the dataset already exists
        # TODO: Prawal make a HTTP request or use message queues
        dataset_db = await get_dataset(digital_contract_req.dataset_id, current_user)
        if dataset_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

        dataset_db = Dataset_Db(**dataset_db)

        # Add the digital contract to the database
        digital_contract_db = DigitalContract_Db(
            **digital_contract_req.dict(),
            data_owner_id=dataset_db.organization_id,
            state=DigitalContractState.NEW,
            researcher_id=current_user.organization_id
        )
        await data_service.insert_one(DB_COLLECTION_DIGITAL_CONTRACTS, jsonable_encoder(digital_contract_db))

        return digital_contract_db
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.get(
    path="/digital-contracts",
    description="Get list of all the digital_contract",
    response_description="List of digital_contract",
    response_model=List[GetDigitalContract_Out],
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_all_digital_contract(
    data_owner_id: Optional[PyObjectId] = None,
    researcher_id: Optional[PyObjectId] = None,
    current_user: TokenData = Depends(get_current_user),
):
    try:
        # TODO: Prawal the current user organization is repeated in the request, find a better way
        if (data_owner_id is not None) and (data_owner_id == current_user.organization_id):
            query = {"data_owner_id": str(data_owner_id)}
        elif (researcher_id is not None) and (researcher_id == current_user.organization_id):
            query = {"researcher_id": str(researcher_id)}
        elif current_user.role is UserRole.SAILADMIN:
            query = {}
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        digital_contracts = await data_service.find_by_query(DB_COLLECTION_DIGITAL_CONTRACTS, query)
        return digital_contracts
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.get(
    path="/digital-contracts/{digital_contract_id}",
    description="Get the information about a digital contract",
    response_model=GetDigitalContract_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_digital_contract(digital_contract_id: PyObjectId, current_user: TokenData = Depends(get_current_user)):
    try:
        digital_contract = await data_service.find_one(
            DB_COLLECTION_DIGITAL_CONTRACTS, {"_id": str(digital_contract_id)}
        )
        if digital_contract is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Digital Contract not found")

        digital_contract_db = DigitalContract_Db(**digital_contract)
        if (
            (digital_contract_db.data_owner_id != current_user.organization_id)
            and (digital_contract_db.researcher_id != current_user.organization_id)
            and (current_user.role != UserRole.SAILADMIN)
        ):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        return digital_contract
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.put(
    path="/digital-contracts/{digital_contract_id}",
    description="Update digital contract information",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_digital_contract(
    digital_contract_id: PyObjectId,
    updated_digital_contract_info: UpdateDigitalContract_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
):
    try:
        # Check if the digital contract exists
        digital_contract_db = await data_service.find_one(
            DB_COLLECTION_DIGITAL_CONTRACTS, {"_id": str(digital_contract_id)}
        )
        if digital_contract_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Digital Contract not found")

        digital_contract_db = DigitalContract_Db(**digital_contract_db)

        # Only a new digital contract information can be updated by the researcher
        # Data Owner can only accept or reject a request
        # Only researcher can activate a digital contract
        if digital_contract_db.state == DigitalContractState.NEW:
            # Only information can be updated by the researcher
            if digital_contract_db.researcher_id == current_user.organization_id:
                if updated_digital_contract_info.name is not None:
                    digital_contract_db.name = updated_digital_contract_info.name
                if updated_digital_contract_info.description is not None:
                    digital_contract_db.description = updated_digital_contract_info.description
                if updated_digital_contract_info.subscription_days is not None:
                    digital_contract_db.subscription_days = updated_digital_contract_info.subscription_days
                if updated_digital_contract_info.legal_agreement is not None:
                    digital_contract_db.legal_agreement = updated_digital_contract_info.legal_agreement
                if updated_digital_contract_info.version is not None:
                    digital_contract_db.version = updated_digital_contract_info.version
            # data owner can only accept the request
            elif digital_contract_db.data_owner_id == current_user.organization_id:
                if updated_digital_contract_info.state == DigitalContractState.ACCEPTED:
                    digital_contract_db.state = DigitalContractState.ACCEPTED
                else:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
            # All other requests are invalid on a new digital contract
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        elif digital_contract_db.state == DigitalContractState.ACCEPTED:
            # Only researcher can activate a digital contract
            if digital_contract_db.researcher_id != current_user.organization_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
            if updated_digital_contract_info.state != DigitalContractState.ACTIVATED:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
            digital_contract_db.state = DigitalContractState.ACTIVATED

        else:
            # An activated digital contract can not be updated
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        await data_service.update_one(
            DB_COLLECTION_DIGITAL_CONTRACTS,
            {"_id": str(digital_contract_id)},
            {"$set": jsonable_encoder(digital_contract_db)},
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.delete(
    path="/digital-contracts/{digital_contract_id}",
    description="Disable the digital_contract",
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN]))],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def soft_delete_digital_contract(
    digital_contract_id: PyObjectId, current_user: TokenData = Depends(get_current_user)
):
    try:
        # Check if the digital contract exists
        digital_contract_db = await data_service.find_one(
            DB_COLLECTION_DIGITAL_CONTRACTS, {"_id": str(digital_contract_id)}
        )
        if digital_contract_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Digital Contract not found")

        digital_contract_db = DigitalContract_Db(**digital_contract_db)

        # Only dataownwer or researcher can disable a digital contract
        if (
            digital_contract_db.data_owner_id != current_user.organization_id
            and digital_contract_db.researcher_id != current_user.organization_id
        ):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        if (
            digital_contract_db.state == DigitalContractState.NEW
            and digital_contract_db.data_owner_id == current_user.organization_id
        ):
            # A new digital contract can be rejected by the data owner
            digital_contract_db.state = DigitalContractState.REJECTED
        else:
            # TODO: Prawal when is a digital contract archived?
            # Other times it is archived
            digital_contract_db.state = DigitalContractState.ARCHIVED

        # Update the digital contract
        await data_service.update_one(
            DB_COLLECTION_DIGITAL_CONTRACTS,
            {"_id": str(digital_contract_id)},
            {"$set": jsonable_encoder(digital_contract_db)},
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception