########################################################################################################################
# @author Prawal Gangwar
# @brief APIs to manage data-federations
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
########################################################################################################################

from typing import List, Optional

from app.api.accounts import get_organization
from app.api.authentication import RoleChecker, get_current_user
from app.api.datasets_families import get_dataset_family
from app.data import operations as data_service
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from models.accounts import UserRole
from models.authentication import TokenData
from models.common import BasicObjectInfo, PyObjectId
from models.data_federations import (
    DataFederation_Db,
    DataFederationState,
    GetDataFederation_Out,
    GetMultipleDataFederation_Out,
    RegisterDataFederation_In,
    RegisterDataFederation_Out,
    UpdateDataFederation_In,
)

DB_COLLECTION_DATA_FEDERATIONS = "data-federations"

router = APIRouter()


def getForgetPasswordContent(secret: str):
    htmlText = (
        """
        <html>
            <head></head>
            <body>
                Hello, <br><br> <br>Visit to reset your password:
                    <a href = "http://www.secureailabs.com">http://www.secureailabs.com/"""
        + secret
        + """</a>
            </body>
        </html>
    """
    )
    return htmlText


########################################################################################################################
@router.post(
    path="/data-federations",
    description="Register new data federation",
    response_description="DataFederation Id",
    response_model=RegisterDataFederation_Out,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
)
async def register_data_federation(
    data_federation_req: RegisterDataFederation_In = Body(...), current_user: TokenData = Depends(get_current_user)
):
    try:
        # Add the data federation to the database
        data_federation_db = DataFederation_Db(
            **data_federation_req.dict(), organization_id=current_user.organization_id, state=DataFederationState.ACTIVE
        )
        await data_service.insert_one(DB_COLLECTION_DATA_FEDERATIONS, jsonable_encoder(data_federation_db))

        return data_federation_db
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.get(
    path="/data-federations",
    description="Get list of all the data federations",
    response_description="List of data federations",
    response_model=GetMultipleDataFederation_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_all_data_federations(
    data_submitter_id: Optional[PyObjectId] = None,
    researcher_id: Optional[PyObjectId] = None,
    data_families_id: Optional[PyObjectId] = None,
    current_user: TokenData = Depends(get_current_user),
):
    try:
        if (data_submitter_id) and (data_submitter_id == current_user.organization_id):
            query = {"data_submitter_id": {"$all": [str(current_user.organization_id)]}}
        elif (researcher_id) and (researcher_id == current_user.organization_id):
            query = {"researcher_id": {"$all": [str(current_user.organization_id)]}}
        elif data_families_id:
            query = {"researcher_id": {"$all": [str(data_families_id)]}}
        elif current_user.role is UserRole.SAIL_ADMIN:
            query = {}
        elif (not data_submitter_id) and (not researcher_id) and (not data_families_id):
            query = {
                "$or": [
                    {"organization_id": str(current_user.organization_id)},
                    {"data_submitter_organizations_id": {"$all": [str(current_user.organization_id)]}},
                    {"research_organizations_id": {"$all": [str(current_user.organization_id)]}},
                ]
            }
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        data_federations = await data_service.find_by_query(DB_COLLECTION_DATA_FEDERATIONS, query)

        response_list_of_data_federations: List[GetDataFederation_Out] = []

        # Cache the organization information
        organization_cache = {}
        data_family_cache = {}
        # Add the organization information to the data federation
        for data_federation in data_federations:
            data_federation = DataFederation_Db(**data_federation)
            if data_federation.organization_id not in organization_cache:
                organization_cache[data_federation.organization_id] = await get_organization(
                    organization_id=data_federation.organization_id, current_user=current_user
                )

            data_submitter_basic_info_list: List[BasicObjectInfo] = []
            for data_submitter in data_federation.data_submitter_organizations_id:
                if data_submitter not in organization_cache:
                    organization_cache[data_submitter] = await get_organization(
                        organization_id=data_submitter, current_user=current_user
                    )
                data_submitter_basic_info_list.append(organization_cache[data_submitter])

            researcher_basic_info_list: List[BasicObjectInfo] = []
            for researcher in data_federation.research_organizations_id:
                if researcher not in organization_cache:
                    organization_cache[researcher] = await get_organization(
                        organization_id=researcher, current_user=current_user
                    )
                researcher_basic_info_list.append(organization_cache[researcher])

            data_family_basic_info_list: List[BasicObjectInfo] = []
            for data_family in data_federation.dataset_families_id:
                if data_family not in data_family_cache:
                    data_family_cache[data_family] = await get_dataset_family(
                        dataset_family_id=data_family, current_user=current_user
                    )
                data_family_basic_info_list.append(data_family_cache[data_family])

            respose_data_federation = GetDataFederation_Out(
                **data_federation.dict(),
                organization=organization_cache[data_federation.organization_id],
                data_submitter_organizations=data_submitter_basic_info_list,
                research_organizations=researcher_basic_info_list,
                dataset_families=data_family_basic_info_list,
                invites=[]
            )
            response_list_of_data_federations.append(respose_data_federation)

        return GetMultipleDataFederation_Out(data_federations=response_list_of_data_federations)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.get(
    path="/data-federations/{data_federation_id}",
    description="Get the information about a data federation",
    response_model=GetDataFederation_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_data_federation(data_federation_id: PyObjectId, current_user: TokenData = Depends(get_current_user)):
    try:
        data_federation = await data_service.find_one(DB_COLLECTION_DATA_FEDERATIONS, {"_id": str(data_federation_id)})
        if not data_federation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DataFederation not found")

        data_federation = DataFederation_Db(**data_federation)
        organization = await get_organization(
            organization_id=data_federation.organization_id, current_user=current_user
        )

        data_submitter_basic_info_list: List[BasicObjectInfo] = []
        for data_submitter in data_federation.data_submitter_organizations_id:
            data_submitter_organization = await get_organization(
                organization_id=data_submitter, current_user=current_user
            )
            data_submitter_basic_info_list.append(data_submitter_organization)

        researcher_basic_info_list: List[BasicObjectInfo] = []
        for researcher in data_federation.research_organizations_id:
            researcher_organization = await get_organization(organization_id=researcher, current_user=current_user)
            researcher_basic_info_list.append(researcher_organization)

        data_family_basic_info_list: List[BasicObjectInfo] = []
        for data_family in data_federation.dataset_families_id:
            data_family = await get_dataset_family(dataset_family_id=data_family, current_user=current_user)
            data_family_basic_info_list.append(data_family)

        respose_data_federation = GetDataFederation_Out(
            **data_federation.dict(),
            organization=organization,
            data_submitter_organizations=data_submitter_basic_info_list,
            research_organizations=researcher_basic_info_list,
            dataset_families=data_family_basic_info_list,
            invites=[]
        )

        return respose_data_federation
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.put(
    path="/data-federations/{data_federation_id}",
    description="Update data federation information",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_data_federation(
    data_federation_id: PyObjectId,
    updated_data_federation_info: UpdateDataFederation_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
):
    try:
        # DataFederation must be part of same organization
        data_federation_db = await data_service.find_one(
            DB_COLLECTION_DATA_FEDERATIONS, {"_id": str(data_federation_id)}
        )
        if not data_federation_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DataFederation not found")

        data_federation_db = DataFederation_Db(**data_federation_db)
        if data_federation_db.organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        # TODO: Prawal find better way to update the data federation
        if updated_data_federation_info.description:
            data_federation_db.description = updated_data_federation_info.description

        if updated_data_federation_info.name:
            data_federation_db.name = updated_data_federation_info.name

        await data_service.update_one(
            DB_COLLECTION_DATA_FEDERATIONS,
            {"_id": str(data_federation_id)},
            {"$set": jsonable_encoder(data_federation_db)},
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.put(
    path="/data-federations/{data_federation_id}/researcher/{organization_id}",
    description="Invite a researcher to join a data federation",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def invite_researcher(
    data_federation_id: PyObjectId, organization_id: PyObjectId, current_user: TokenData = Depends(get_current_user)
):
    try:
        data_federation_db = await data_service.find_one(
            DB_COLLECTION_DATA_FEDERATIONS,
            {"_id": str(data_federation_id), "organization_id": str(current_user.organization_id)},
        )
        if not data_federation_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DataFederation not found")

        data_federation_db = DataFederation_Db(**data_federation_db)
        # If the organization is already part of the data federation, then return 200 OK
        if (organization_id in data_federation_db.research_organizations_id) or (
            organization_id in data_federation_db.invites_id
        ):
            return Response(status_code=status.HTTP_200_OK)

        # If the organization is not part of the data federation, then add it to the invites list
        data_federation_db.invites_id.append(organization_id)

        # Create a background process to send the invitation email

        await data_service.update_one(
            DB_COLLECTION_DATA_FEDERATIONS,
            {"_id": str(data_federation_id)},
            {"$set": jsonable_encoder(data_federation_db)},
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.delete(
    path="/data-federations/{data_federation_id}",
    description="Disable the data federation",
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN]))],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def soft_delete_data_federation(
    data_federation_id: PyObjectId, current_user: TokenData = Depends(get_current_user)
):
    try:
        # DataFederation must be part of same organization
        data_federation_db = await data_service.find_one(
            DB_COLLECTION_DATA_FEDERATIONS, {"_id": str(data_federation_id)}
        )
        if not data_federation_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DataFederation not found")

        data_federation_db = DataFederation_Db(**data_federation_db)
        if data_federation_db.organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        # Disable the data federation
        data_federation_db.state = DataFederationState.INACTIVE
        await data_service.update_one(
            DB_COLLECTION_DATA_FEDERATIONS,
            {"_id": str(data_federation_id)},
            {"$set": jsonable_encoder(data_federation_db)},
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception
