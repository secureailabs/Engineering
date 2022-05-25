########################################################################################################################
# @author Prawal Gangwar
# @brief APIs to manage digital contracts
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
########################################################################################################################

from typing import Optional

from app.api.accounts import get_organization
from app.api.authentication import RoleChecker, get_current_user
from app.api.datasets import get_dataset
from app.data import operations as data_service
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from models.accounts import UserRole
from models.authentication import TokenData
from models.common import PyObjectId
from models.datasets import GetDataset_Out
from models.digital_contracts import (
    DigitalContract_Db,
    DigitalContractState,
    GetDigitalContract_Out,
    GetMultipleDigitalContract_Out,
    RegisterDigitalContract_In,
    RegisterDigitalContract_Out,
    UpdateDigitalContract_In,
)

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
        if not dataset_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

        dataset_db = GetDataset_Out(**dataset_db)

        # Add the digital contract to the database
        digital_contract_db = DigitalContract_Db(
            **digital_contract_req.dict(),
            data_owner_id=dataset_db.organization.id,
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
    response_model=GetMultipleDigitalContract_Out,
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
        if (data_owner_id) and (data_owner_id == current_user.organization_id):
            query = {"data_owner_id": str(data_owner_id)}
        elif (researcher_id) and (researcher_id == current_user.organization_id):
            query = {"researcher_id": str(researcher_id)}
        elif current_user.role is UserRole.SAIL_ADMIN:
            query = {}
        elif (not researcher_id) and (not data_owner_id):
            query = {
                "$or": [
                    {"researcher_id": str(current_user.organization_id)},
                    {"data_owner_id": str(current_user.organization_id)},
                ]
            }
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        digital_contracts = await data_service.find_by_query(DB_COLLECTION_DIGITAL_CONTRACTS, query)

        # Cache the organization information
        organization_cache = {}
        dataset_cache = {}

        for digital_contract in digital_contracts:
            # Add the data owner organization information to the dataset
            if digital_contract["data_owner_id"] not in organization_cache:
                organization_cache[digital_contract["data_owner_id"]] = await get_organization(
                    organization_id=digital_contract["data_owner_id"], current_user=current_user
                )
            digital_contract["data_owner"] = organization_cache[digital_contract["data_owner_id"]]
            digital_contract.pop("data_owner_id")

            # Add the researcher organization information to the dataset
            if digital_contract["researcher_id"] not in organization_cache:
                organization_cache[digital_contract["researcher_id"]] = await get_organization(
                    organization_id=digital_contract["researcher_id"], current_user=current_user
                )
            digital_contract["researcher"] = organization_cache[digital_contract["researcher_id"]]
            digital_contract.pop("researcher_id")

            # Add the dataset information to the dataset
            if digital_contract["dataset_id"] not in dataset_cache:
                organization_cache[digital_contract["dataset_id"]] = await get_dataset(
                    dataset_id=digital_contract["dataset_id"], current_user=current_user
                )
            digital_contract["dataset"] = organization_cache[digital_contract["dataset_id"]]
            digital_contract.pop("dataset_id")

        return GetMultipleDigitalContract_Out(digital_contracts=digital_contracts)
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
        if not digital_contract:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Digital Contract not found")

        digital_contract_db = DigitalContract_Db(**digital_contract)
        if (
            (digital_contract_db.data_owner_id != current_user.organization_id)
            and (digital_contract_db.researcher_id != current_user.organization_id)
            and (current_user.role != UserRole.SAIL_ADMIN)
        ):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        # Add the data owner organization information to the dataset
        digital_contract["data_owner"] = await get_organization(
            organization_id=digital_contract["data_owner_id"], current_user=current_user
        )
        digital_contract.pop("data_owner_id")

        # Add the researcher organization information to the dataset
        digital_contract["researcher"] = await get_organization(
            organization_id=digital_contract["researcher_id"], current_user=current_user
        )
        digital_contract.pop("researcher_id")

        # Add the dataset information to the dataset
        digital_contract["dataset"] = await get_dataset(
            dataset_id=digital_contract["dataset_id"], current_user=current_user
        )
        digital_contract.pop("dataset_id")

        return GetDigitalContract_Out(**digital_contract)
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
        if not digital_contract_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Digital Contract not found")

        digital_contract_db = DigitalContract_Db(**digital_contract_db)

        # Only a new digital contract information can be updated by the researcher
        # Data Owner can only accept or reject a request
        # Only researcher can activate a digital contract
        if digital_contract_db.state == DigitalContractState.NEW:
            # Only information can be updated by the researcher
            if digital_contract_db.researcher_id == current_user.organization_id:
                if updated_digital_contract_info.name:
                    digital_contract_db.name = updated_digital_contract_info.name
                if updated_digital_contract_info.description:
                    digital_contract_db.description = updated_digital_contract_info.description
                if updated_digital_contract_info.subscription_days:
                    digital_contract_db.subscription_days = updated_digital_contract_info.subscription_days
                if updated_digital_contract_info.legal_agreement:
                    digital_contract_db.legal_agreement = updated_digital_contract_info.legal_agreement
                if updated_digital_contract_info.version:
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
        if not digital_contract_db:
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
