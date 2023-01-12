# -------------------------------------------------------------------------------
# Engineering
# authentication.py
# -------------------------------------------------------------------------------
"""Sail authentication and authorization service"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

from time import time
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import parse_obj_as

from app.data import operations as data_service
from app.log import log_message
from app.utils.secrets import get_secret
from models.accounts import Organization_db, User_Db, UserInfo_Out, UserRole
from models.authentication import LoginSuccess_Out, RefreshToken_In, TokenData, TokenScope
from models.common import BasicObjectInfo, PyObjectId

DB_COLLECTION_USERS = "users"
DB_COLLECTION_ORGANIZATIONS = "organizations"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

# Authentication settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_password_hash(
    salt: str,
    password: str,
):
    password_pepper = get_secret("password_pepper")
    return pwd_context.hash(f"{salt}{password}{password_pepper}")


def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_secret("jwt_secret"), algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
        user_id = token_data.id
        if not user_id:
            raise credentials_exception
    except JWTError as exception:
        raise credentials_exception
    return token_data


########################################################################################################################
class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: TokenData = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")


########################################################################################################################
class ScopeChecker:
    def __init__(self, allowed_scope: List[TokenScope]):
        self.allowed_scopes = allowed_scope

    def __call__(self, user: TokenData = Depends(get_current_user)):
        if user.scope not in self.allowed_scopes:
            raise HTTPException(status_code=403, detail="Operation not permitted")


def create_jwt_token(
    user_id: PyObjectId,
    organization_id: PyObjectId,
    role: UserRole,
    scope: List[TokenScope],
    expiry_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
    key: str = get_secret("jwt_secret"),
):
    token_data = TokenData(
        id=user_id,
        organization_id=organization_id,
        role=role,
        scope=scope,
        exp=int(time() + expiry_minutes * 60),
    )

    return jwt.encode(
        claims=jsonable_encoder(token_data),
        key=key,
        algorithm=ALGORITHM,
    )


########################################################################################################################
@router.post(
    path="/login",
    description="User login with email and password",
    response_model=LoginSuccess_Out,
    response_model_by_alias=False,
    operation_id="login",
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> LoginSuccess_Out:
    """
    User login with email and password

    :param form_data: input data for user login with email, password and scope
    :type form_data: OAuth2PasswordRequestForm, optional
    :return: access token and refresh token
    :rtype: LoginSuccess_Out
    """
    exception_authentication_failed = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password or scope",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Scope is required
    if not form_data.scopes:
        raise exception_authentication_failed

    # The scopes should be among the scopes for this endpoint, the other scopes are generated elsewhere
    if not set(form_data.scopes).issubset(set(["COMPUTE", "DATASET", "ACCOUNT"])):
        raise exception_authentication_failed

    found_user = await data_service.find_one(DB_COLLECTION_USERS, {"email": form_data.username})
    if not found_user:
        raise exception_authentication_failed

    found_user_db = User_Db(**found_user)
    password_pepper = get_secret("password_pepper")
    if not pwd_context.verify(
        f"{found_user_db.email}{form_data.password}{password_pepper}", found_user_db.hashed_password
    ):
        raise exception_authentication_failed

    access_token = create_jwt_token(
        user_id=found_user_db.id,
        organization_id=found_user_db.organization_id,
        role=found_user_db.role,
        expiry_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        scope=parse_obj_as(List[TokenScope], form_data.scopes),
    )

    refresh_token = create_jwt_token(
        user_id=found_user_db.id,
        organization_id=found_user_db.organization_id,
        role=found_user_db.role,
        key=get_secret("refresh_secret"),
        expiry_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        scope=parse_obj_as(List[TokenScope], form_data.scopes),
    )

    message = f"[Login For Access Token]: user_email:{form_data.username}"
    await log_message(message)

    return LoginSuccess_Out(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


########################################################################################################################
@router.post(
    path="/refresh-token",
    description="Refresh the JWT token for the user",
    response_model=LoginSuccess_Out,
    operation_id="get_refresh_token",
)
async def refresh_for_access_token(
    refresh_token_request: RefreshToken_In = Body(description="Refresh token request"),
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials."
    )
    try:
        # TODO: Prawal harden the security around the refresh token
        payload = jwt.decode(refresh_token_request.refresh_token, get_secret("refresh_secret"), algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
        user_id = token_data.id
        if not user_id:
            raise credentials_exception

        found_user = await data_service.find_one(DB_COLLECTION_USERS, {"_id": str(user_id)})
        if not found_user:
            raise credentials_exception

        found_user_db = User_Db(**found_user)
        access_token = create_jwt_token(
            user_id=found_user_db.id,
            organization_id=found_user_db.organization_id,
            role=found_user_db.role,
            expiry_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
            scope=token_data.scope,
        )

        refresh_token = create_jwt_token(
            user_id=found_user_db.id,
            organization_id=found_user_db.organization_id,
            role=found_user_db.role,
            key=get_secret("refresh_secret"),
            expiry_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
            scope=token_data.scope,
        )

        message = f"[Refresh For Access Token]: user_id: {user_id}"
        await log_message(message)

    except JWTError as exception:
        raise credentials_exception

    return LoginSuccess_Out(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


########################################################################################################################
@router.get(
    path="/me",
    description="Get the current user information",
    response_description="The current user information",
    response_model=UserInfo_Out,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
    operation_id="get_current_user_info",
)
async def get_current_user_info(
    current_user: TokenData = Depends(get_current_user),
) -> UserInfo_Out:
    """
    Get the current user information

    :param current_user: The current user information
    :type current_user: TokenData, optional
    :return: The current user information
    :rtype: UserInfo_Out
    """

    found_user = await data_service.find_one(DB_COLLECTION_USERS, {"_id": str(current_user.id)})
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")
    found_user_db = User_Db(**found_user)

    # Get the user organization information
    found_organization = await data_service.find_one(
        DB_COLLECTION_ORGANIZATIONS, {"_id": str(found_user_db.organization_id)}
    )
    if not found_organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    found_organization_db = Organization_db(**found_organization)

    message = f"[Get Current User Info]: user_id:{current_user.id}"
    await log_message(message)

    return UserInfo_Out(**found_user, organization=BasicObjectInfo(**found_organization), scope=current_user.scope)
