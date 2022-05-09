########################################################################################################################
# @author Prawal Gangwar
# @brief APIs to manage user accounts and organizations
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
########################################################################################################################

from typing import List
from fastapi import APIRouter, Depends, Body, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from models.authentication import TokenData
from models.accounts import (
    GetOrganizations_Out,
    GetUsers_Out,
    OrganizationState,
    RegisterOrganization_In,
    Organization_db,
    RegisterOrganization_Out,
    RegisterUser_In,
    RegisterUser_Out,
    UpdateOrganization_In,
    UpdateUser_In,
    User_Db,
    UserRole,
    UserAccountState,
)
from models.common import PyObjectId
from app.api.authentication import RoleChecker, get_current_user, get_password_hash
from app.data import operations as data_service

########################################################################################################################
DB_COLLECTION_ORGANIZATIONS = "organizations"
DB_COLLECTION_USERS = "users"

router = APIRouter()


########################################################################################################################
@router.post(
    path="/organizations",
    description="Register new organization and the admin user",
    response_description="Organization Id",
    response_model=RegisterOrganization_Out,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
)
async def register_organization(organization: RegisterOrganization_In = Body(...)):
    try:
        # Check if the admin is already registered
        user_db = await data_service.find_one(DB_COLLECTION_USERS, {"email": organization.admin_email})
        if user_db is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already registered")

        # Add the organization to the database if it doesn't already exists
        organization_db = Organization_db(**organization.dict(), organization_state=OrganizationState.ACTIVE)
        await data_service.insert_one(DB_COLLECTION_ORGANIZATIONS, jsonable_encoder(organization_db))

        # Create an admin user account
        admin_user_db = User_Db(
            username=organization.admin_name,
            email=organization.admin_email,
            job_title=organization.admin_job_title,
            role=UserRole.ADMIN,
            hashed_password=get_password_hash(organization.admin_email, organization.admin_password),
            account_state=UserAccountState.ACTIVE,
            organization_id=organization_db.id,
            avatar=organization.admin_avatar,
        )

        admin_user = await data_service.insert_one(DB_COLLECTION_USERS, jsonable_encoder(admin_user_db))
        print(admin_user)

        return organization_db
    except HTTPException as http_exception:
        # return the response to the client with proper message as this was an expected error
        raise http_exception
    except Exception as exception:
        # This is not returned to the client and instead recoreded in the logs database to be investigated
        # the sail admin can always login and look at these logs to see when and what went wrong
        # return internal server error+id to the user and log the error
        raise exception


########################################################################################################################
@router.get(
    path="/organizations",
    description="Get list of all the organizations",
    response_description="List of organizations",
    response_model=List[GetOrganizations_Out],
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.SAILADMIN]))],
    status_code=status.HTTP_200_OK,
)
async def get_all_organizations(current_user: TokenData = Depends(get_current_user)):
    try:
        organizations = await data_service.find_all(DB_COLLECTION_ORGANIZATIONS)
        return organizations
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.get(
    path="/organizations/{organization_id}",
    description="Get the information about a organization",
    response_model=GetOrganizations_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_organization(organization_id: PyObjectId, current_user: TokenData = Depends(get_current_user)):
    try:
        organization = await data_service.find_one(DB_COLLECTION_ORGANIZATIONS, {"_id": str(organization_id)})
        if organization is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        return organization
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.put(
    path="/organizations/{organization_id}",
    description="Update organization information",
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN]))],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_organization(
    organization_id: PyObjectId,
    update_organization_info: UpdateOrganization_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
):
    try:
        # User must be part of same organization
        if organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        organization_db = await data_service.find_one(DB_COLLECTION_ORGANIZATIONS, {"_id": str(organization_id)})
        if organization_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

        organization_db = Organization_db(**organization_db)
        if update_organization_info.name is not None:
            organization_db.name = update_organization_info.name

        if update_organization_info.description is not None:
            organization_db.description = update_organization_info.description

        if update_organization_info.avatar is not None:
            organization_db.avatar = update_organization_info.avatar

        await data_service.update_one(
            DB_COLLECTION_ORGANIZATIONS, {"_id": str(organization_id)}, {"$set": jsonable_encoder(organization_db)}
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.delete(
    path="/organizations/{organization_id}",
    description="Disable the organization and all the users",
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN]))],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def soft_delete_organization(organization_id: PyObjectId, current_user: TokenData = Depends(get_current_user)):
    try:
        # User must be part of same organization
        if organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        # TODO: Transaction. Make this atomic transaction
        # Check if the organization exists
        organization_db = await data_service.find_one(DB_COLLECTION_ORGANIZATIONS, {"_id": str(organization_id)})
        if organization_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

        # Disable all the users except admin
        users = await data_service.find_by_query(DB_COLLECTION_USERS, {"organization_id": str(organization_id)})
        for user in users:
            user_db = User_Db(**user)
            if user_db.role != UserRole.ADMIN:
                user_db.account_state = UserAccountState.INACTIVE
                await data_service.update_one(
                    DB_COLLECTION_USERS, {"_id": str(user_db.id)}, {"$set": jsonable_encoder(user_db)}
                )

        # Disable the organization
        organization_db = Organization_db(**organization_db)
        organization_db.organization_state = OrganizationState.INACTIVE
        await data_service.update_one(
            DB_COLLECTION_ORGANIZATIONS, {"_id": str(organization_id)}, {"$set": jsonable_encoder(organization_db)}
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.post(
    path="/organizations/{organization_id}/users",
    description="Add new user to organization",
    response_model=RegisterUser_Out,
    response_model_by_alias=False,
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN]))],
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    organization_id: PyObjectId,
    user: RegisterUser_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
):
    try:
        # User must be part of same organization
        if organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        # Check if the user already exists
        user_db = await data_service.find_one(DB_COLLECTION_USERS, {"email": str(user.email)})
        if user_db is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

        # Create the user and add it to the database
        user_db = User_Db(
            **user.dict(),
            hashed_password=get_password_hash(user.email, user.password),
            organization_id=organization_id,
            account_state=UserAccountState.ACTIVE
        )

        await data_service.insert_one(DB_COLLECTION_USERS, jsonable_encoder(user_db))

        return user_db
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.get(
    path="/organizations/{organization_id}/users",
    description="Get all users in the organization",
    response_model=List[GetUsers_Out],
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN, UserRole.SAILADMIN]))],
    status_code=status.HTTP_200_OK,
)
async def get_users(organization_id: PyObjectId, current_user: TokenData = Depends(get_current_user)):
    try:
        # User must be part of same organization
        if organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        users = await data_service.find_by_query(DB_COLLECTION_USERS, {"organization_id": str(organization_id)})
        return users
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.get(
    path="/organizations/{organization_id}/users/{user_id}",
    description="Get information about a user",
    response_model=GetUsers_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    organization_id: PyObjectId, user_id: PyObjectId, current_user: TokenData = Depends(get_current_user)
):
    try:
        # User must be part of same organization
        if organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        # Check if the user exists
        user_db = await data_service.find_one(
            DB_COLLECTION_USERS, {"_id": str(user_id), "organization_id": str(organization_id)}
        )
        if user_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user_db
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.put(
    path="/organizations/{organization_id}/users/{user_id}",
    description="Update user information",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_user_info(
    organization_id: PyObjectId,
    user_id: PyObjectId,
    update_user_info: UpdateUser_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
):
    try:
        # User must be part of same organization
        if organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        # Check if the user exists
        user = await data_service.find_one(
            DB_COLLECTION_USERS, {"_id": str(user_id), "organization_id": str(organization_id)}
        )
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user_db = User_Db(**user)
        # Only admin can update the role and account state
        if current_user.role is UserRole.ADMIN:
            if update_user_info.role is not None:
                user_db.role = update_user_info.role
            if update_user_info.account_state is not None:
                user_db.account_state = update_user_info.account_state

        # Other info can be updated by the same user only
        if current_user.id == user_id:
            if update_user_info.job_title is not None:
                user_db.job_title = update_user_info.job_title
            if update_user_info.avatar is not None:
                user_db.avatar = update_user_info.avatar

        await data_service.update_one(
            DB_COLLECTION_USERS,
            {"_id": str(user_id), "organization_id": str(organization_id)},
            {"$set": jsonable_encoder(user_db)},
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.delete(
    path="/organizations/{organization_id}/users/{user_id}",
    description="Soft Delete user",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def soft_delete_user(
    organization_id: PyObjectId, user_id: PyObjectId, current_user: TokenData = Depends(get_current_user)
):
    try:
        # User must be part of same organization
        if organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

        # Only admin or user can delete the user
        if current_user.role is UserRole.ADMIN or current_user.id is user_id:
            # Check if the user exists
            user = await data_service.find_one(
                DB_COLLECTION_USERS, {"_id": str(user_id), "organization_id": str(organization_id)}
            )
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            user_db = User_Db(**user)
            user_db.account_state = UserAccountState.INACTIVE
            await data_service.update_one(
                DB_COLLECTION_USERS,
                {"_id": str(user_id), "organization_id": str(organization_id)},
                {"$set": jsonable_encoder(user_db)},
            )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception
