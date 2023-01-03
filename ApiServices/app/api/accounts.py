# -------------------------------------------------------------------------------
# Engineering
# accounts.py
# -------------------------------------------------------------------------------
"""APIs to manage user accounts and organizations"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------


from fastapi import APIRouter, Body, Depends, HTTPException, Path, Response, status
from fastapi.encoders import jsonable_encoder

from app.api.authentication import RoleChecker, get_current_user, get_password_hash
from app.data import operations as data_service
from app.log import log_message
from models.accounts import (
    GetMultipleOrganizations_Out,
    GetMultipleUsers_Out,
    GetOrganizations_Out,
    GetUsers_Out,
    Organization_db,
    OrganizationState,
    RegisterOrganization_In,
    RegisterOrganization_Out,
    RegisterUser_In,
    RegisterUser_Out,
    UpdateOrganization_In,
    UpdateUser_In,
    User_Db,
    UserAccountState,
    UserRole,
)
from models.authentication import TokenData
from models.common import BasicObjectInfo, PyObjectId

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
    operation_id="register_organization",
)
async def register_organization(
    organization: RegisterOrganization_In = Body(description="Organization details"),
):
    # Check if the admin is already registered
    user_db = await data_service.find_one(DB_COLLECTION_USERS, {"email": organization.admin_email})
    if user_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already registered")

    # Add the organization to the database if it doesn't already exists
    organization_db = Organization_db(**organization.dict(), state=OrganizationState.ACTIVE)
    await data_service.insert_one(DB_COLLECTION_ORGANIZATIONS, jsonable_encoder(organization_db))

    # Create an admin user account
    admin_user_db = User_Db(
        name=organization.admin_name,
        email=organization.admin_email,
        job_title=organization.admin_job_title,
        role=UserRole.ADMIN,
        hashed_password=get_password_hash(organization.admin_email, organization.admin_password),
        account_state=UserAccountState.ACTIVE,
        organization_id=organization_db.id,
        avatar=organization.admin_avatar,
    )

    await data_service.insert_one(DB_COLLECTION_USERS, jsonable_encoder(admin_user_db))

    message = f"[Organization Register]: name:{organization.admin_name}, email:{organization.admin_email}, job_title:{organization.admin_job_title}"
    await log_message(message)

    return organization_db


########################################################################################################################
@router.get(
    path="/organizations",
    description="Get list of all the organizations",
    response_description="List of organizations",
    response_model=GetMultipleOrganizations_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.SAIL_ADMIN]))],
    status_code=status.HTTP_200_OK,
    operation_id="get_all_organizations",
)
async def get_all_organizations(current_user: TokenData = Depends(get_current_user)):
    organizations = await data_service.find_all(DB_COLLECTION_ORGANIZATIONS)

    message = f"[Get All Organizations]: user_id:{current_user.id}"
    await log_message(message)

    return GetMultipleOrganizations_Out(organizations=organizations)


########################################################################################################################
@router.get(
    path="/organizations/{organization_id}",
    description="Get the information about a organization",
    response_model=GetOrganizations_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    operation_id="get_organization",
)
async def get_organization(
    organization_id: PyObjectId = Path(description="UUID of the requested organization"),
    current_user: TokenData = Depends(get_current_user),
) -> GetOrganizations_Out:
    organization = await data_service.find_one(DB_COLLECTION_ORGANIZATIONS, {"_id": str(organization_id)})
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    message = f"[Get Organizaton]: user_id:{current_user.id}, organization:{organization_id}"
    await log_message(message)

    return GetOrganizations_Out(**organization)  # type: ignore


########################################################################################################################
@router.put(
    path="/organizations/{organization_id}",
    description="Update organization information",
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN]))],
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="update_organization",
)
async def update_organization(
    organization_id: PyObjectId = Path(description="UUID of the requested organization"),
    update_organization_info: UpdateOrganization_In = Body(description="Organization details to update"),
    current_user: TokenData = Depends(get_current_user),
):
    # User must be part of same organization
    if organization_id != current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    organization_db = await data_service.find_one(DB_COLLECTION_ORGANIZATIONS, {"_id": str(organization_id)})
    if not organization_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    organization_db = Organization_db(**organization_db)
    if update_organization_info.name:
        organization_db.name = update_organization_info.name

    if update_organization_info.description:
        organization_db.description = update_organization_info.description

    if update_organization_info.avatar:
        organization_db.avatar = update_organization_info.avatar

    await data_service.update_one(
        DB_COLLECTION_ORGANIZATIONS, {"_id": str(organization_id)}, {"$set": jsonable_encoder(organization_db)}
    )

    message = f"[Organization Update]: user_id:{current_user.id}, organization_id:{organization_id}, update_organization_info:{update_organization_info}"
    await log_message(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################################################################################################################
@router.delete(
    path="/organizations/{organization_id}",
    description="Disable the organization and all the users",
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN]))],
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="soft_delete_organization",
)
async def soft_delete_organization(
    organization_id: PyObjectId = Path(description="UUID of the organization to be deleted"),
    current_user: TokenData = Depends(get_current_user),
):
    # User must be part of same organization
    if organization_id != current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    # TODO: Transaction. Make this atomic transaction
    # Check if the organization exists
    organization_db = await data_service.find_one(DB_COLLECTION_ORGANIZATIONS, {"_id": str(organization_id)})
    if not organization_db:
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
    organization_db = Organization_db(**organization_db)  # type: ignore
    organization_db.organization_state = OrganizationState.INACTIVE
    await data_service.update_one(
        DB_COLLECTION_ORGANIZATIONS, {"_id": str(organization_id)}, {"$set": jsonable_encoder(organization_db)}
    )

    message = f"[Organization Soft Delete]: user_id:{current_user.id}, organization_id:{organization_id}"
    await log_message(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################################################################################################################
@router.post(
    path="/organizations/{organization_id}/users",
    description="Add new user to organization",
    response_model=RegisterUser_Out,
    response_model_by_alias=False,
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN]))],
    status_code=status.HTTP_201_CREATED,
    operation_id="register_user",
)
async def register_user(
    organization_id: PyObjectId = Path(description="UUID of the organization to add the user to"),
    user: RegisterUser_In = Body(description="User details to register with the organization"),
    current_user: TokenData = Depends(get_current_user),
):
    # User must be part of same organization
    if organization_id != current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    # Check if the user already exists
    user_db = await data_service.find_one(DB_COLLECTION_USERS, {"email": str(user.email)})
    if user_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    # Create the user and add it to the database
    user_db = User_Db(
        **user.dict(),
        hashed_password=get_password_hash(user.email, user.password),
        organization_id=organization_id,
        account_state=UserAccountState.ACTIVE,
    )

    await data_service.insert_one(DB_COLLECTION_USERS, jsonable_encoder(user_db))

    message = f"[Register User]: user_id:{current_user.id}, user_email:{user.email}"
    await log_message(message)

    return user_db


########################################################################################################################
@router.get(
    path="/organizations/{organization_id}/users",
    description="Get all users in the organization",
    response_model=GetMultipleUsers_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN, UserRole.SAIL_ADMIN]))],
    status_code=status.HTTP_200_OK,
    operation_id="get_users",
)
async def get_users(
    organization_id: PyObjectId = Path(description="UUID of the organization"),
    current_user: TokenData = Depends(get_current_user),
):
    # User must be part of same organization
    if organization_id != current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    # Get the organization information
    organization_db = await data_service.find_one(DB_COLLECTION_ORGANIZATIONS, {"_id": str(organization_id)})
    if not organization_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User organization not found")
    organization_db = Organization_db(**organization_db)  # type: ignore

    users = await data_service.find_by_query(DB_COLLECTION_USERS, {"organization_id": str(organization_id)})

    # Add organization to each element in the list
    for user in users:
        user["organization"] = organization_db
        # Remove the organization_id field
        user.pop("organization_id")

    message = f"[Get Users]: user_id:{current_user.id}, users:{users}"
    await log_message(message)

    return GetMultipleUsers_Out(users=users)  # type: ignore


########################################################################################################################
async def get_all_admins(organization_id: PyObjectId) -> GetMultipleUsers_Out:
    """
    Private internal call to get all the admins of an organization

    :param organization_id: organization for which admins are requested
    :type organization_id: PyObjectId
    :raises HTTPException: HTTP_404_NOT_FOUND, "User organization not found"
    :raises HTTPException: HTTP_404_NOT_FOUND, "Organization admins not found"
    :raises exception: 500, internal server error
    :return: list of admins of the organizations
    :rtype: GetMultipleUsers_Out
    """
    # Get the organization information
    organization_db = await data_service.find_one(DB_COLLECTION_ORGANIZATIONS, {"_id": str(organization_id)})
    if not organization_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User organization not found")
    organization_db = Organization_db(**organization_db)  # type: ignore

    users = await data_service.find_by_query(
        DB_COLLECTION_USERS, {"organization_id": str(organization_id), "role": "ADMIN"}
    )
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization admins not found")

    # Add organization to each element in the list
    for user in users:
        user["organization"] = organization_db
        # Remove the organization_id field
        user.pop("organization_id")

    message = f"[Get All Admins]"
    await log_message(message)

    return GetMultipleUsers_Out(users=users)  # type: ignore


########################################################################################################################
@router.get(
    path="/organizations/{organization_id}/users/{user_id}",
    description="Get information about a user",
    response_model=GetUsers_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(RoleChecker(allowed_roles=[UserRole.ADMIN, UserRole.SAIL_ADMIN]))],
    operation_id="get_user",
)
async def get_user(
    organization_id: PyObjectId = Path(description="UUID of the organization"),
    user_id: PyObjectId = Path(description="UUID of the user"),
    current_user: TokenData = Depends(get_current_user),
):
    # Check if the user exists
    user_db = await data_service.find_one(
        DB_COLLECTION_USERS, {"_id": str(user_id), "organization_id": str(organization_id)}
    )
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_db = User_Db(**user_db)  # type: ignore

    # Get the organization information
    organization_db = await data_service.find_one(DB_COLLECTION_ORGANIZATIONS, {"_id": str(user_db.organization_id)})
    if not organization_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User organization not found")
    organization_db = Organization_db(**organization_db)  # type: ignore

    message = f"[Get Users]: user_id:{current_user.id}"
    await log_message(message)

    return GetUsers_Out(**user_db.dict(), organization=BasicObjectInfo(**organization_db.dict()))


########################################################################################################################
@router.put(
    path="/organizations/{organization_id}/users/{user_id}",
    description="Update user information",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="update_user_info",
)
async def update_user_info(
    organization_id: PyObjectId = Path(description="UUID of the organization"),
    user_id: PyObjectId = Path(description="UUID of the user"),
    update_user_info: UpdateUser_In = Body(description="User information to update"),
    current_user: TokenData = Depends(get_current_user),
):
    # User must be part of same organization
    if organization_id != current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    # Check if the user exists
    user = await data_service.find_one(
        DB_COLLECTION_USERS, {"_id": str(user_id), "organization_id": str(organization_id)}
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_db = User_Db(**user)  # type: ignore
    # Only admin can update the role and account state
    if current_user.role is UserRole.ADMIN:
        if update_user_info.role:
            user_db.role = update_user_info.role
        if update_user_info.account_state:
            user_db.account_state = update_user_info.account_state

    # Other info can be updated by the same user only
    if current_user.id == user_id:
        if update_user_info.job_title:
            user_db.job_title = update_user_info.job_title
        if update_user_info.avatar:
            user_db.avatar = update_user_info.avatar

    await data_service.update_one(
        DB_COLLECTION_USERS,
        {"_id": str(user_id), "organization_id": str(organization_id)},
        {"$set": jsonable_encoder(user_db)},
    )

    message = f"[Update User Info], user_id:{current_user.id}, updated_target:{user_id}, updated_target_info: {update_user_info}"
    await log_message(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################################################################################################################
@router.delete(
    path="/organizations/{organization_id}/users/{user_id}",
    description="Soft Delete user",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="soft_delete_user",
)
async def soft_delete_user(
    organization_id: PyObjectId = Path(description="UUID of the organization"),
    user_id: PyObjectId = Path(description="UUID of the user"),
    current_user: TokenData = Depends(get_current_user),
):
    # User must be part of same organization
    if organization_id != current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    # Only admin or user can delete the user
    if current_user.role is UserRole.ADMIN or current_user.id is user_id:
        # Check if the user exists
        user = await data_service.find_one(
            DB_COLLECTION_USERS, {"_id": str(user_id), "organization_id": str(organization_id)}
        )
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user_db = User_Db(**user)  # type: ignore
        user_db.account_state = UserAccountState.INACTIVE
        await data_service.update_one(
            DB_COLLECTION_USERS,
            {"_id": str(user_id), "organization_id": str(organization_id)},
            {"$set": jsonable_encoder(user_db)},
        )

    message = f"[Soft Delete User]: user_id:{current_user.id}, deleted_user:{user_id}"

    return Response(status_code=status.HTTP_204_NO_CONTENT)
