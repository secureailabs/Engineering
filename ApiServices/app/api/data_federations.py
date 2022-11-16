# -------------------------------------------------------------------------------
# Engineering
# data_federations.py
# -------------------------------------------------------------------------------
"""APIs to manage data-federations"""

# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr

import app.utils.azure as azure
from app.api.accounts import get_all_admins, get_organization, get_user
from app.api.authentication import RoleChecker, get_current_user
from app.api.datasets import get_dataset, get_datset_encryption_key
from app.api.emails import send_email
from app.api.internal_utils import cache_get_basic_info_datasets, cache_get_basic_info_organization
from app.data import operations as data_service
from app.log import log_message
from models.accounts import GetUsers_Out, UserRole
from models.authentication import TokenData
from models.common import BasicObjectInfo, KeyVaultObject, PyObjectId
from models.data_federations import (
    DataFederation_Db,
    DataFederationState,
    DataSubmitterIdKeyPair,
    GetDataFederation_Out,
    GetInvite_Out,
    GetMultipleDataFederation_Out,
    GetMultipleInvite_Out,
    Invite_Db,
    InviteState,
    InviteType,
    PatchInvite_In,
    RegisterDataFederation_In,
    RegisterDataFederation_Out,
    RegisterInvite_In,
    RegisterInvite_Out,
    UpdateDataFederation_In,
)
from models.datasets import DatasetEncryptionKey_Out
from models.emails import EmailRequest

DB_COLLECTION_DATA_FEDERATIONS = "data-federations"
DB_COLLECTION_INVITES = "data-federation-invites"

router = APIRouter()


def getEmailInviteContent(data_federation: str, inviter_organization: str) -> str:
    """
    Generate the body of the email invite

    :param data_federation: the name of the data federation
    :type data_federation: str
    :param inviter_organization: the name of the inviter organization
    :type inviter_organization: str
    :return: HTML body of the email
    :rtype: str
    """
    htmlText = f"""
        <html>
            <head></head>
            <body>
                Hello, <br><br> <br>Hi, You are invited to be part of data federation {data_federation} by {inviter_organization}. Kindly visit:
                    <a href = "http://www.secureailabs.com">http://www.secureailabs.com/invites</a> to respond to the invitation.
            </body>
        </html>
    """

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
    # Add the data federation to the database
    data_federation_db = DataFederation_Db(
        **data_federation_req.dict(), organization_id=current_user.organization_id, state=DataFederationState.ACTIVE
    )
    await data_service.insert_one(DB_COLLECTION_DATA_FEDERATIONS, jsonable_encoder(data_federation_db))

    message = f"[Register Data Federation]: user_id:{current_user.id}"
    await log_message(message)

    return data_federation_db


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
    dataset_id: Optional[PyObjectId] = None,
    current_user: TokenData = Depends(get_current_user),
) -> GetMultipleDataFederation_Out:
    if (data_submitter_id) and (data_submitter_id == current_user.organization_id):
        query = ({"data_submitters.organization_id": str(current_user.organization_id)},)
    elif (researcher_id) and (researcher_id == current_user.organization_id):
        query = {"researcher_id": {"$all": [str(current_user.organization_id)]}}
    elif dataset_id:
        query = {"dataset_id": {"$all": [str(dataset_id)]}}
    elif current_user.role is UserRole.SAIL_ADMIN:
        query = {}
    elif (not data_submitter_id) and (not researcher_id) and (not dataset_id):
        query = {
            "$or": [
                {"organization_id": str(current_user.organization_id)},
                {"data_submitters.organization_id": str(current_user.organization_id)},
                {"research_organizations_id": {"$all": [str(current_user.organization_id)]}},
            ]
        }
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    data_federations = await data_service.find_by_query(DB_COLLECTION_DATA_FEDERATIONS, query)

    response_list_of_data_federations: List[GetDataFederation_Out] = []

    # Cache the organization information
    organization_cache: Dict[PyObjectId, BasicObjectInfo] = {}
    dataset_cache: Dict[PyObjectId, BasicObjectInfo] = {}

    # Add the organization information to the data federation
    for data_federation in data_federations:
        data_federation = DataFederation_Db(**data_federation)

        # Add the organization information to the data federation
        organization_cache, data_submitter_basic_info_list = await cache_get_basic_info_organization(
            organization_cache, [data_federation.organization_id], current_user
        )

        # Add the data submitter organization information to the data federation
        organization_cache, data_submitter_basic_info_list = await cache_get_basic_info_organization(
            organization_cache,
            [data_submitter.organization_id for data_submitter in data_federation.data_submitters],
            current_user,
        )

        # Add the research organization information to the data federation
        organization_cache, researcher_basic_info_list = await cache_get_basic_info_organization(
            organization_cache, data_federation.research_organizations_id, current_user
        )

        # Add the dataset information to the data federation
        dataset_cache, dataset_basic_info_list = await cache_get_basic_info_datasets(
            dataset_cache, data_federation.datasets_id, current_user
        )

        response_data_federation = GetDataFederation_Out(
            **data_federation.dict(),
            organization=organization_cache[data_federation.organization_id],
            data_submitter_organizations=data_submitter_basic_info_list,
            research_organizations=researcher_basic_info_list,
            datasets=dataset_basic_info_list,
        )
        response_list_of_data_federations.append(response_data_federation)

    message = f"[Get All Data Federations]: user_id: {current_user.id}"
    await log_message(message)

    return GetMultipleDataFederation_Out(data_federations=response_list_of_data_federations)


########################################################################################################################
@router.get(
    path="/data-federations/{data_federation_id}",
    description="Get the information about a data federation",
    response_model=GetDataFederation_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_data_federation(
    data_federation_id: PyObjectId, current_user: TokenData = Depends(get_current_user)
) -> GetDataFederation_Out:
    data_federation = await data_service.find_one(DB_COLLECTION_DATA_FEDERATIONS, {"_id": str(data_federation_id)})
    if not data_federation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DataFederation not found")

    data_federation = DataFederation_Db(**data_federation)

    # Add the organization information to the data federation
    _, organization = await cache_get_basic_info_organization({}, [data_federation.organization_id], current_user)

    _, data_submitter_basic_info_list = await cache_get_basic_info_organization(
        {}, [data_submitter.organization_id for data_submitter in data_federation.data_submitters], current_user
    )

    _, researcher_basic_info_list = await cache_get_basic_info_organization(
        {}, data_federation.research_organizations_id, current_user
    )

    # Add the dataset information to the data federation
    _, dataset_basic_info_list = await cache_get_basic_info_datasets({}, data_federation.datasets_id, current_user)

    response_data_federation = GetDataFederation_Out(
        **data_federation.dict(),
        organization=organization[0],
        data_submitter_organizations=data_submitter_basic_info_list,
        research_organizations=researcher_basic_info_list,
        datasets=dataset_basic_info_list,
    )

    message = f"[Get Data Federation]: user_id: {current_user.id}, data_federatuon_id: {data_federation_id}"
    await log_message(message)

    return response_data_federation


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
    # DataFederation must be part of same organization
    data_federation_db = await data_service.find_one(DB_COLLECTION_DATA_FEDERATIONS, {"_id": str(data_federation_id)})
    if not data_federation_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DataFederation not found")

    data_federation_db = DataFederation_Db(**data_federation_db)
    if data_federation_db.organization_id != current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    if updated_data_federation_info.description:
        data_federation_db.description = updated_data_federation_info.description

    if updated_data_federation_info.name:
        data_federation_db.name = updated_data_federation_info.name

    await data_service.update_one(
        DB_COLLECTION_DATA_FEDERATIONS,
        {"_id": str(data_federation_id)},
        {"$set": jsonable_encoder(data_federation_db)},
    )

    message = f"[Update Data Federation]: user_id:{current_user.id}"
    await log_message(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################################################################################################################
@router.put(
    path="/data-federations/{data_federation_id}/researcher/{researcher_organization_id}",
    description="Invite a researcher to join a data federation",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def invite_researcher(
    background_tasks: BackgroundTasks,
    data_federation_id: PyObjectId,
    researcher_organization_id: PyObjectId,
    current_user: TokenData = Depends(get_current_user),
):
    """
    Invite a researcher to join a data federation

    :param background_tasks: FastAPI will create the object of type BackgroundTasks and pass it as that parameter
    :type background_tasks: BackgroundTasks
    :param data_federation_id: data federation for which the invitation is being made
    :type data_federation_id: PyObjectId
    :param researcher_organization_id: the researcher organization that is being invited
    :type researcher_organization_id: PyObjectId
    :param current_user: the information about the current user accessed from JWT, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :raises HTTPException: HTTP_404_NOT_FOUND, "DataFederation not found"
    :raises HTTPException: HTTP_401_UNAUTHORIZED, "Unauthorised"
    :raises exception: should be 500, internal server error
    :return: None
    :rtype: None
    """
    # Only data federation owner can invite invite other organizations
    data_federation_db = await data_service.find_one(
        DB_COLLECTION_DATA_FEDERATIONS,
        {"_id": str(data_federation_id), "organization_id": str(current_user.organization_id)},
    )
    if not data_federation_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DataFederation not found")
    data_federation_db = DataFederation_Db(**data_federation_db)

    # If the organization is already part of the data federation, then return 204 OK
    if researcher_organization_id in data_federation_db.research_organizations_id:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # If the organization is not part of the data federation, add it to the invites list
    invite_req = RegisterInvite_In(
        data_federation_id=data_federation_id,
        inviter_user_id=current_user.id,
        inviter_organization_id=current_user.organization_id,
        invitee_organization_id=researcher_organization_id,
        type=InviteType.DF_RESEARCHER,
    )

    add_invite_response = await register_invite(invite_req=invite_req)
    data_federation_db.research_organizations_invites_id.append(add_invite_response.id)

    # Get the current/inviter organization information
    inviter_organization = await get_organization(current_user.organization_id, current_user)

    # Get list of all the admins of the invited organization
    admin_users = await get_all_admins(researcher_organization_id)
    admin_user_emails: List[EmailStr] = []
    for admin in admin_users.users:
        admin_user_emails.append(admin.email)

    # Create a background process to send the invitation email
    background_tasks.add_task(
        send_invite_email,
        "SAIL: Invitation to join Data Federation as Researcher",
        getEmailInviteContent(data_federation=data_federation_db.name, inviter_organization=inviter_organization.name),
        admin_user_emails,
    )

    await data_service.update_one(
        DB_COLLECTION_DATA_FEDERATIONS,
        {"_id": str(data_federation_id)},
        {"$set": jsonable_encoder(data_federation_db)},
    )

    message = f"[Invite Researcher]: user_id:{current_user.id}, data_federation_id: {data_federation_id}, organization_id: {researcher_organization_id}"
    await log_message(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################################################################################################################
@router.post(
    path="/data-federations/{data_federation_id}/data-submitter/{data_submitter_organization_id}",
    description="Automatically add a data submitter to the data federation, bypassing an invite path",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def register_data_submitter(
    data_federation_id: PyObjectId,
    data_submitter_organization_id: PyObjectId,
    current_user: TokenData = Depends(get_current_user),
):
    """
    Register a data submitter to an organization - This is an internal call for SAIL to manage a federation

    :param data_federation_id: data federation for which the data submitter is being registered
    :type data_federation_id: PyObjectId
    :param data_submitter_organization_id: the data submitter organization that is being registered
    :type data_submitter_organization_id: PyObjectId
    :param current_user: the information about the current user accessed from JWT, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :raises HTTPException: HTTP_404_NOT_FOUND, "DataFederation not found"
    :raises HTTPException: HTTP_401_UNAUTHORIZED, "Unauthorised"
    :raises exception: should be 500, internal server error
    :return: None
    :rtype: None
    """
    data_federation_db = await data_service.find_one(
        DB_COLLECTION_DATA_FEDERATIONS,
        {"_id": str(data_federation_id), "organization_id": str(current_user.organization_id)},
    )
    if not data_federation_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DataFederation not found")
    data_federation_db = DataFederation_Db(**data_federation_db)

    # If the organization is already part of the data federation, then return 204 OK
    if data_submitter_organization_id in [
        data_submitter.organization_id for data_submitter in data_federation_db.data_submitters
    ]:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # Ensure this is a valid organization before adding to the list
    _, organization = await cache_get_basic_info_organization({}, [data_submitter_organization_id], current_user)

    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    # Generate RSA key vault keys and update with their handles
    key_name = f"{str(data_federation_id)}-{str(organization[0].id)}"
    data_submitter_key = generate_rsa_key(key_name)

    # Add the data submitter to the federation list
    data_submitter_key_pair = DataSubmitterIdKeyPair(
        organization_id=data_submitter_organization_id,
        key=data_submitter_key,
    )

    data_federation_db.data_submitters.append(data_submitter_key_pair)

    await data_service.update_one(
        DB_COLLECTION_DATA_FEDERATIONS,
        {"_id": str(data_federation_id)},
        {"$set": jsonable_encoder(data_federation_db)},
    )

    message = f"[Register Data Submitter]: user_id:{current_user.id}, data_federation_id: {data_federation_id}, data_submitter_id: {data_submitter_organization_id}"
    await log_message(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################################################################################################################
@router.post(
    path="/data-federations/{data_federation_id}/researcher/{researcher_organization_id}",
    description="Automatically add a researcher to the data federation, bypassing an invite path",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def register_researcher(
    data_federation_id: PyObjectId,
    researcher_organization_id: PyObjectId,
    current_user: TokenData = Depends(get_current_user),
):
    """
    Register a researcher to an organization - This is an internal call for SAIL to manage a federation

    :param data_federation_id: data federation for which the data submitter is being registered
    :type data_federation_id: PyObjectId
    :param researcher_organization_id: the researcher organization that is being registered
    :type researcher_organization_id: PyObjectId
    :param current_user: the information about the current user accessed from JWT, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :raises HTTPException: HTTP_404_NOT_FOUND, "DataFederation not found"
    :raises HTTPException: HTTP_401_UNAUTHORIZED, "Unauthorised"
    :raises exception: should be 500, internal server error
    :return: None
    :rtype: None
    """
    data_federation_db = await data_service.find_one(
        DB_COLLECTION_DATA_FEDERATIONS,
        {"_id": str(data_federation_id), "organization_id": str(current_user.organization_id)},
    )
    if not data_federation_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DataFederation not found")
    data_federation_db = DataFederation_Db(**data_federation_db)

    # If the organization is already part of the data federation, then return 204 OK
    if researcher_organization_id in data_federation_db.research_organizations_id:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # Ensure this is a valid organization before adding to the list
    _, organization = await cache_get_basic_info_organization({}, [researcher_organization_id], current_user)

    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    # Add the researcher to the researcher list
    data_federation_db.research_organizations_id.append(researcher_organization_id)

    await data_service.update_one(
        DB_COLLECTION_DATA_FEDERATIONS,
        {"_id": str(data_federation_id)},
        {"$set": jsonable_encoder(data_federation_db)},
    )

    message = f"[Register Researcher]: user_id:{current_user.id}, data_federation_id: {data_federation_id}, researcher_id: {researcher_organization_id}"
    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################################################################################################################
@router.put(
    path="/data-federations/{data_federation_id}/data-submitter/{data_submitter_organization_id}",
    description="Invite a data submitter to join a data federation",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def invite_data_submitter(
    background_tasks: BackgroundTasks,
    data_federation_id: PyObjectId,
    data_submitter_organization_id: PyObjectId,
    current_user: TokenData = Depends(get_current_user),
):
    """
    Invite a data submitter to join a data federation

    :param background_tasks: FastAPI will create the object of type BackgroundTasks and pass it as that parameter
    :type background_tasks: BackgroundTasks
    :param data_federation_id: data federation for which the invitation is being made
    :type data_federation_id: PyObjectId
    :param data_submitter_organization_id: the data submitter organization that is being invited
    :type data_submitter_organization_id: PyObjectId
    :param current_user: the information about the current user accessed from JWT, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :raises HTTPException: HTTP_404_NOT_FOUND, "DataFederation not found"
    :raises HTTPException: HTTP_401_UNAUTHORIZED, "Unauthorised"
    :raises exception: should be 500, internal server error
    :return: None
    :rtype: None
    """
    # Only data federation owner can invite invite other organizations
    data_federation_db = await data_service.find_one(
        DB_COLLECTION_DATA_FEDERATIONS,
        {"_id": str(data_federation_id), "organization_id": str(current_user.organization_id)},
    )
    if not data_federation_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DataFederation not found")
    data_federation_db = DataFederation_Db(**data_federation_db)

    # If the organization is already part of the data federation, then return 204 OK
    if data_submitter_organization_id in [
        data_submitter.organization_id for data_submitter in data_federation_db.data_submitters
    ]:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # If the organization is not part of the data federation, add it to the invites list
    invite_req = RegisterInvite_In(
        data_federation_id=data_federation_id,
        inviter_user_id=current_user.id,
        inviter_organization_id=current_user.organization_id,
        invitee_organization_id=data_submitter_organization_id,
        type=InviteType.DF_SUBMITTER,
    )

    add_invite_response = await register_invite(invite_req=invite_req)
    data_federation_db.data_submitter_organizations_invites_id.append(add_invite_response.id)

    # Get the current/inviter organization information
    inviter_organization = await get_organization(current_user.organization_id, current_user)

    # Get list of all the admins of the invited organization
    admin_users = await get_all_admins(data_submitter_organization_id)
    admin_user_emails: List[EmailStr] = []
    for admin in admin_users.users:
        admin_user_emails.append(admin.email)

    # Create a background process to send the invitation email
    background_tasks.add_task(
        send_invite_email,
        "SAIL: Invitation to join Data Federation as Data Submitter",
        getEmailInviteContent(data_federation=data_federation_db.name, inviter_organization=inviter_organization.name),
        admin_user_emails,
    )

    await data_service.update_one(
        DB_COLLECTION_DATA_FEDERATIONS,
        {"_id": str(data_federation_id)},
        {"$set": jsonable_encoder(data_federation_db)},
    )

    message = f"[Invite Data Submitter]: user_id:{current_user.id}, data_federation_id: {data_federation_id}, organization_id: {data_submitter_organization_id}"
    await log_message(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


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
    # DataFederation must be part of same organization
    data_federation_db = await data_service.find_one(DB_COLLECTION_DATA_FEDERATIONS, {"_id": str(data_federation_id)})
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

    message = f"[Soft Delete Data Federation]: user_id:{current_user.id}"
    await log_message(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################################################################################################################
async def register_invite(invite_req: RegisterInvite_In):
    """
    Registe and invite to database

    :param invite_req: the information about the invite
    :type invite_req: RegisterInvite_In
    :return: information about the invite
    :rtype: RegisterInvite_Out
    """
    # Add the invite to the database
    created_time = datetime.utcnow()
    # The default expiry time of an invite is 10 days.
    expiry_time = created_time + timedelta(days=10)
    invite_db = Invite_Db(
        **invite_req.dict(), state=InviteState.PENDING, created_time=created_time, expiry_time=expiry_time
    )
    await data_service.insert_one(DB_COLLECTION_INVITES, jsonable_encoder(invite_db))

    message = f"[Register Invite]"
    await log_message(message)

    return RegisterInvite_Out(**invite_db.dict())


########################################################################################################################
@router.get(
    path="/data-federations/{organization_id}/invites",
    description="Get list of all the pending invites received. Only ADMIN roles have access.",
    response_description="List of pending invites received",
    response_model=GetMultipleInvite_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN]))],
)
async def get_all_invites(organization_id: PyObjectId, current_user: TokenData = Depends(get_current_user)):
    """
    Get list of all the pending invites received. Only ADMIN roles have access.

    :param organization_id: organization for which invites are listed
    :type organization_id: PyObjectId
    :param current_user: the information about the current user accessed from JWT, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :raises HTTPException: HTTP_401_UNAUTHORIZED, Unauthorised
    :raises exception: 500, internal server error
    :return: a list of pending invites
    :rtype: GetMultipleInvite_Out
    """
    if organization_id != current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised")

    query = {"invitee_organization_id": str(current_user.organization_id), "state": "PENDING"}
    invites = await data_service.find_by_query(DB_COLLECTION_INVITES, query)

    # Add the inviter information to the invite
    invites_out: List[GetInvite_Out] = []
    for invite in invites:
        invite = Invite_Db(**invite)
        inviter_user: GetUsers_Out = await get_user(
            invite.inviter_organization_id, invite.inviter_user_id, current_user
        )
        data_federation: GetDataFederation_Out = await get_data_federation(invite.data_federation_id)
        invites_out.append(
            GetInvite_Out(
                **invite.dict(),
                data_federation=BasicObjectInfo(**data_federation.dict()),
                inviter_user=BasicObjectInfo(**inviter_user.dict()),
                inviter_organization=inviter_user.organization,
            )
        )

    message = f"[Get All Invites]: user_id:{current_user.id}, organization_id: {organization_id}"
    await log_message(message)

    return GetMultipleInvite_Out(invites=invites_out)


########################################################################################################################
@router.get(
    path="/data-federations/{organization_id}/invites/{invite_id}",
    description="Get the information about an invite",
    response_model=GetInvite_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN]))],
)
async def get_invite(
    organization_id: PyObjectId, invite_id: PyObjectId, current_user: TokenData = Depends(get_current_user)
):
    """
    Get the information about an invite

    :param organization_id: organization for which the invites are listed
    :type organization_id: PyObjectId
    :param invite_id: invite id
    :type invite_id: PyObjectId
    :param current_user: the information about the current user accessed from JWT, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :raises HTTPException: HTTP_401_UNAUTHORIZED, "Unauthorised"
    :raises HTTPException: HTTP_404_NOT_FOUND, "Invite not found"
    :raises exception: 500, internal server error
    :return: the invite information
    :rtype: GetInvite_Out
    """
    if organization_id != current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised")

    invite = await data_service.find_one(DB_COLLECTION_INVITES, {"_id": str(invite_id)})
    if not invite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite not found")
    invite = Invite_Db(**invite)

    inviter_user: GetUsers_Out = await get_user(invite.inviter_organization_id, invite.inviter_user_id, current_user)
    data_federation: GetDataFederation_Out = await get_data_federation(invite.data_federation_id)
    invite_out = GetInvite_Out(
        **invite.dict(),
        data_federation=BasicObjectInfo(**data_federation.dict()),
        inviter_user=BasicObjectInfo(**inviter_user.dict()),
        inviter_organization=inviter_user.organization,
    )

    message = f"[Get Invite]: user_id:{current_user.id}, data_federation_id: {invite.data_federation_id}, invite_id: {invite_id}, organization_id: {organization_id}"
    await log_message(message)

    return invite_out


########################################################################################################################
@router.patch(
    path="/data-federations/{organization_id}/invites/{invite_id}",
    description="Accept or reject an invite",
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN]))],
)
async def accept_or_reject_invite(
    organization_id: PyObjectId,
    invite_id: PyObjectId,
    updated_invite: PatchInvite_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
):
    """
    Accept or reject an invite

    :param organization_id: id of the invited organization
    :type organization_id: PyObjectId
    :param invite_id: invite id
    :type invite_id: PyObjectId
    :param updated_invite: the update information, defaults to Body(...)
    :type updated_invite: PatchInvite_In, optional
    :param current_user: the information about the current user accessed from JWT, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :raises HTTPException: HTTP_401_UNAUTHORIZED, "Unauthorised"
    :raises HTTPException: HTTP_404_NOT_FOUND, "Invite not found"
    :raises exception: 500, internal server error
    :return: status_code=status.HTTP_204_NO_CONTENT
    :rtype: Response
    """
    if organization_id != current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised")

    invite = await data_service.find_one(DB_COLLECTION_INVITES, {"_id": str(invite_id)})
    if not invite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite not found")
    invite = Invite_Db(**invite)

    # Invite should not have expired.
    if invite.expiry_time < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Invite expired")

    # Can only be accepeted or rejected by invitee organization
    if invite.invitee_organization_id != current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    if updated_invite.state is InviteState.ACCEPTED or updated_invite.state is InviteState.REJECTED:
        invite.state = updated_invite.state
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    await data_service.update_one(
        DB_COLLECTION_INVITES,
        {"_id": str(invite_id)},
        {"$set": jsonable_encoder(invite)},
    )

    # Upon acceptance remove the invite from the list of invites in the data federation and add the organization to
    # accepted list
    if invite.state is InviteState.ACCEPTED:
        # Get the data federation
        data_federation = await data_service.find_one(
            DB_COLLECTION_DATA_FEDERATIONS, {"_id": str(invite.data_federation_id)}
        )
        if not data_federation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data federation not found")
        data_federation = DataFederation_Db(**data_federation)

        if invite.type is InviteType.DF_RESEARCHER:
            data_federation.research_organizations_id.append(invite.invitee_organization_id)
            data_federation.research_organizations_invites_id.remove(invite.id)
        if invite.type is InviteType.DF_SUBMITTER:
            # Generate RSA key vault keys and update with their handles
            key_name = f"{str(invite.data_federation_id)}-{str(current_user.organization_id)}"
            data_submitter_key = generate_rsa_key(key_name)

            # Add the data submitter to the federation list
            data_submitter_key_pair = DataSubmitterIdKeyPair(
                organization_id=invite.invitee_organization_id, key=data_submitter_key
            )

            data_federation.data_submitters.append(data_submitter_key_pair)
            data_federation.data_submitter_organizations_invites_id.remove(invite.id)

        await data_service.update_one(
            DB_COLLECTION_DATA_FEDERATIONS,
            {"_id": str(invite.data_federation_id)},
            {"$set": jsonable_encoder(data_federation)},
        )

    message = f"[Accept Or Reject Invite]: user_id:{current_user.id}, data_federation_id: {invite.data_federation_id}, invite_id: {invite_id}"
    await log_message(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################################################################################################################
def send_invite_email(subject: str, email_body: str, emails: List[EmailStr]):
    """
    Background task to send emails using the email plugin

    :param subject: Email subject
    :type subject: str
    :param email_body: body of email
    :type email_body: str
    :param emails: list of email id to send email to
    :type emails: List[EmailStr]
    """
    email_req = EmailRequest(to=emails, subject=subject, body=email_body)
    send_email(email_req)


########################################################################################################################
@router.put(
    path="/data-federations/{data_federation_id}/datasets/{dataset_id}",
    description="Add a dataset to a data federation",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def add_dataset(
    data_federation_id: PyObjectId,
    dataset_id: PyObjectId,
    current_user: TokenData = Depends(get_current_user),
):
    """
    Add a dataset to a data federation

    :param data_federation_id: data federation for which the invitation is being made
    :type data_federation_id: PyObjectId
    :param dataset_id: the dataset id that is being added to the data federation
    :type dataset_id: PyObjectId
    :param current_user: the information about the current user accessed from JWT, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :raises HTTPException: HTTP_404_NOT_FOUND, "DataFederation not found"
    :raises HTTPException: HTTP_401_UNAUTHORIZED, "Unauthorised"
    :raises exception: should be 500, internal server error
    """
    # Only data submitter can add datasets to the federation
    data_federation_db = await data_service.find_one(
        DB_COLLECTION_DATA_FEDERATIONS,
        {
            "_id": str(data_federation_id),
            "data_submitters.organization_id": str(current_user.organization_id),
        },
    )
    if not data_federation_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unauthorised")
    data_federation_db = DataFederation_Db(**data_federation_db)

    # Check if the dataset exists
    dataset_info = await get_dataset(dataset_id=dataset_id, current_user=current_user)

    # Dataset must belong to current organization
    if dataset_info.organization.id != current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised")

    # Add the dataset to the data federation
    if dataset_id not in data_federation_db.datasets_id:
        data_federation_db.datasets_id.append(dataset_id)

    # Update the data federation in the database
    await data_service.update_one(
        DB_COLLECTION_DATA_FEDERATIONS,
        {"_id": str(data_federation_id)},
        {"$set": jsonable_encoder(data_federation_db)},
    )

    message = (
        f"[Add Dataset]: user_id:{current_user.id}, data_federation_id: {data_federation_id}, dataset_id: {dataset_id}"
    )
    await log_message(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################################################################################################################
@router.delete(
    path="/data-federations/{data_federation_id}/datasets/{dataset_id}",
    description="Remove a dataset from a data federation",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_dataset(
    data_federation_id: PyObjectId,
    dataset_id: PyObjectId,
    current_user: TokenData = Depends(get_current_user),
):
    """
    Remove a dataset from a data federation

    :param data_federation_id: data federation for which the invitation is being made
    :type data_federation_id: PyObjectId
    :param dataset_id: the dataset id that is being removed from the data federation
    :type dataset_id: PyObjectId
    :param current_user: the information about the current user accessed from JWT, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :raises HTTPException: HTTP_404_NOT_FOUND, "DataFederation not found"
    :raises HTTPException: HTTP_401_UNAUTHORIZED, "Unauthorised"
    :raises exception: should be 500, internal server error
    """
    # Only data federation owner can remove datasets to the federation
    data_federation_db = await data_service.find_one(
        DB_COLLECTION_DATA_FEDERATIONS,
        {
            "_id": str(data_federation_id),
            "organization_id": {"$all": [str(current_user.organization_id)]},
        },
    )
    if not data_federation_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unauthorised")
    data_federation_db = DataFederation_Db(**data_federation_db)

    # Remove the dataset to the data federation
    if dataset_id in data_federation_db.datasets_id:
        data_federation_db.datasets_id.remove(dataset_id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

    # Update the data federation in the database
    await data_service.update_one(
        DB_COLLECTION_DATA_FEDERATIONS,
        {"_id": str(data_federation_id)},
        {"$set": jsonable_encoder(data_federation_db)},
    )

    message = f"[Remove Dataset]: user_id:{current_user.id}, data_federation_id: {data_federation_id}, dataset_id: {dataset_id}"
    await log_message(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    path="/data-federations/{data_federation_id}/dataset_key/{dataset_id}",
    description="Return a dataset encryption key by either retrieving and unwrapping, or creating",
    response_model=DatasetEncryptionKey_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_201_CREATED,
)
async def get_dataset_key(
    data_federation_id: PyObjectId,
    dataset_id: PyObjectId,
    create_if_not_found: bool = True,
    current_user: TokenData = Depends(get_current_user),
):
    """
    Generate and return a dataset encryption key

    :param data_federation_id: data federation for which the request for a key is being made
    :type data_federation_id: PyObjectId
    :param current_user: the information about the current user accessed from JWT, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :raises HTTPException: HTTP_404_NOT_FOUND, "DataFederation not found"
    :raises HTTPException: HTTP_401_UNAUTHORIZED, "Unauthorised"
    :raises exception: should be 500, internal server error
    """
    # Only data federation submitters can generate keys for this federation
    # And data federation researchers cannot generate new keys
    data_federation_db = await data_service.find_one(
        DB_COLLECTION_DATA_FEDERATIONS,
        {
            "_id": str(data_federation_id),
            "$or": [
                {"data_submitters.organization_id": str(current_user.organization_id)},
                {"research_organizations_id": {"$all": [str(current_user.organization_id)]}},
            ],
        },
    )
    if not data_federation_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unauthorised")
    data_federation_db = DataFederation_Db(**data_federation_db)

    # Assume the data_submitter is the current user
    data_submitter_id = current_user.organization_id

    # If the current user is a data researcher, don't allow them to generate new keys
    data_researchers_info = [
        data_researcher
        for data_researcher in data_federation_db.research_organizations_id
        if data_researcher == current_user.organization_id
    ]
    if data_researchers_info:
        create_if_not_found = False
        # Get the data submitter information from the dataset
        dataset_db = await get_dataset(dataset_id=dataset_id, current_user=current_user)
        data_submitter_id = dataset_db.organization.id

    # At this point the data_submitter_id should be set with the correct organization id
    data_submitters_info = [
        data_submitter
        for data_submitter in data_federation_db.data_submitters
        if data_submitter.organization_id == data_submitter_id
    ]
    # Throw an error if the current user is not a data submitter or researcher
    if not data_submitters_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is neither researcher nor submitter")

    # Get the dataset encryption key
    key_info = await get_datset_encryption_key(
        dataset_id=dataset_id,
        wrapping_key=data_submitters_info[0].key,
        create_if_doesnt_exit=create_if_not_found,
        current_user=current_user,
    )

    return key_info


@router.get(
    path="/data-federations/{data_federation_id}/dataset_key/{dataset_id}",
    description="Return a dataset encryption key by either retrieving and unwrapping",
    response_model=DatasetEncryptionKey_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_201_CREATED,
)
async def get_existing_dataset_key(
    data_federation_id: PyObjectId,
    dataset_id: PyObjectId,
    current_user: TokenData = Depends(get_current_user),
):
    """
    Generate and return a dataset encryption key

    :param data_federation_id: data federation for which the request for a key is being made
    :type data_federation_id: PyObjectId
    :param current_user: the information about the current user accessed from JWT, defaults to Depends(get_current_user)
    :type current_user: TokenData, optional
    :raises HTTPException: HTTP_404_NOT_FOUND, "DataFederation not found"
    :raises HTTPException: HTTP_401_UNAUTHORIZED, "Unauthorised"
    :raises exception: should be 500, internal server error
    """
    message = (
        f"[Dataset Key]: user_id:{current_user.id}, data_federation_id: {data_federation_id}, dataset_id: {dataset_id}"
    )
    await log_message(message)

    return await get_dataset_key(
        data_federation_id=data_federation_id,
        dataset_id=dataset_id,
        current_user=current_user,
        create_if_not_found=False,
    )


def generate_rsa_key(key_name: str) -> KeyVaultObject:
    """
    Generate an RSA key pair and return the public key

    :param key_name: the name of the key
    :type key_name: str
    :return: the generated key pair id
    :rtype: str
    """
    account_credentials = azure.authenticate()
    key_client_version = azure.create_rsa_key(account_credentials, key_name, 4096)

    if key_client_version is None:
        raise Exception("Failed to create rsa key")

    return key_client_version
