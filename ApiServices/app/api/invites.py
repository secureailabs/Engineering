########################################################################################################################
# @author Prawal Gangwar
# @brief APIs to manage invites
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
########################################################################################################################

from typing import Optional

from app.api.accounts import get_organization
from app.api.authentication import RoleChecker, get_current_user
from app.data import operations as data_service
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from models.accounts import UserRole
from models.authentication import TokenData
from models.common import PyObjectId
from models.invites import (
    GetInvite_Out,
    GetMultipleInvite_Out,
    Invite_Db,
    InviteState,
    RegisterInvite_In,
    RegisterInvite_Out,
    UpdateInvite_In,
)

DB_COLLECTION_INVITES = "invites"

router = APIRouter()


########################################################################################################################
async def register_invite(
    invite_req: RegisterInvite_In = Body(...), current_user: TokenData = Depends(get_current_user)
):
    try:
        # Check if the invite is already registered
        invite_db = await data_service.find_one(DB_COLLECTION_INVITES, {"_id": str(invite_req.id)})
        if invite_db:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invite already registered")

        # Add the invite to the database
        invite_db = Invite_Db(
            **invite_req.dict(), organization_id=current_user.organization_id, state=InviteState.ACTIVE
        )
        await data_service.insert_one(DB_COLLECTION_INVITES, jsonable_encoder(invite_db))

        return invite_db
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
async def get_all_invites(
    data_owner_id: Optional[PyObjectId] = None,
    current_user: TokenData = Depends(get_current_user),
):
    try:
        # TODO: Prawal the current user organization is repeated in the request, find a better way
        if data_owner_id:
            query = {"data_owner_id": str(data_owner_id)}
        else:
            query = {}

        invites = await data_service.find_by_query(DB_COLLECTION_INVITES, query)

        # Cache the organization information
        organization_cache = {}
        # Add the organization information to the invite
        for invite in invites:
            if invite["organization_id"] not in organization_cache:
                organization_cache[invite["organization_id"]] = await get_organization(
                    organization_id=invite["organization_id"], current_user=current_user
                )
            invite["organization"] = organization_cache[invite["organization_id"]]
            invite.pop("organization_id")

        return GetMultipleInvite_Out(invites=invites)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
async def get_invite(invite_id: PyObjectId, current_user: TokenData = Depends(get_current_user)):
    try:
        invite = await data_service.find_one(DB_COLLECTION_INVITES, {"_id": str(invite_id)})
        if not invite:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite not found")

        # Add the organization information to the invite
        organization_info = await get_organization(organization_id=invite["organization_id"], current_user=current_user)
        invite["organization"] = organization_info
        invite.pop("organization_id")

        return invite
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
async def update_invite(
    invite_id: PyObjectId,
    updated_invite_info: UpdateInvite_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
):
    try:
        # Invite must be part of same organization
        invite_db = await data_service.find_one(DB_COLLECTION_INVITES, {"_id": str(invite_id)})
        if not invite_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite not found")

        invite_db = Invite_Db(**invite_db)
        if invite_db.organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        # TODO: Prawal find better way to update the invite
        if updated_invite_info.description:
            invite_db.description = updated_invite_info.description

        if updated_invite_info.name:
            invite_db.name = updated_invite_info.name

        if updated_invite_info.version:
            invite_db.version = updated_invite_info.version

        if updated_invite_info.keywords:
            invite_db.keywords = updated_invite_info.keywords

        await data_service.update_one(
            DB_COLLECTION_INVITES, {"_id": str(invite_id)}, {"$set": jsonable_encoder(invite_db)}
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
async def soft_delete_invite(invite_id: PyObjectId, current_user: TokenData = Depends(get_current_user)):
    try:
        # Invite must be part of same organization
        invite_db = await data_service.find_one(DB_COLLECTION_INVITES, {"_id": str(invite_id)})
        if not invite_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite not found")

        invite_db = Invite_Db(**invite_db)
        if invite_db.organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        # Disable the invite
        invite_db.state = InviteState.INACTIVE
        await data_service.update_one(
            DB_COLLECTION_INVITES, {"_id": str(invite_id)}, {"$set": jsonable_encoder(invite_db)}
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception
