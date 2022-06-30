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

from app.data import operations as data_service
from app.utils.secrets import get_secret
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from models.accounts import Organization_db, User_Db, UserInfo_Out, UserRole
from models.authentication import LoginSuccess_Out, RefreshToken_In, TokenData
from models.common import BasicObjectInfo
from passlib.context import CryptContext

DB_COLLECTION_USERS = "users"
DB_COLLECTION_ORGANIZATIONS = "organizations"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

# Authentication settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_password_hash(salt, password):
    password_pepper = get_secret("password_pepper")
    return pwd_context.hash(f"{salt}{password}{password_pepper}")


async def get_current_user(token: str = Depends(oauth2_scheme)):
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
@router.post(
    path="/login",
    description="User login with email and password",
    response_model=LoginSuccess_Out,
    response_model_by_alias=False,
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    exception_authentication_failed = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    found_user = await data_service.find_one(DB_COLLECTION_USERS, {"email": form_data.username})
    if not found_user:
        raise exception_authentication_failed

    found_user_db = User_Db(**found_user)
    password_pepper = get_secret("password_pepper")
    if not pwd_context.verify(
        f"{found_user_db.email}{form_data.password}{password_pepper}", found_user_db.hashed_password
    ):
        raise exception_authentication_failed

    token_data = TokenData(**found_user_db.dict(), exp=int((time() * 1000) + (ACCESS_TOKEN_EXPIRE_MINUTES * 60 * 1000)))

    access_token = jwt.encode(
        claims=jsonable_encoder(token_data),
        key=get_secret("jwt_secret"),
        algorithm=ALGORITHM,
    )

    refresh_token = jwt.encode(
        claims=jsonable_encoder(token_data),
        key=get_secret("refresh_secret"),
        algorithm=ALGORITHM,
    )

    return LoginSuccess_Out(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


########################################################################################################################
@router.post(path="/refresh-token", description="Refresh the JWT token for the user", response_model=LoginSuccess_Out)
async def refresh_for_access_token(refresh_token_request: RefreshToken_In = Body(...)):

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
        token_data = TokenData(
            **found_user_db.dict(), exp=int((time() * 1000) + (ACCESS_TOKEN_EXPIRE_MINUTES * 60 * 1000))
        )

        access_token = jwt.encode(
            claims=jsonable_encoder(token_data),
            key=get_secret("jwt_secret"),
            algorithm=ALGORITHM,
        )

        refresh_token = jwt.encode(
            claims=jsonable_encoder(token_data),
            key=get_secret("refresh_secret"),
            algorithm=ALGORITHM,
        )

    except JWTError as exception:
        raise credentials_exception
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception

    return LoginSuccess_Out(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


########################################################################################################################
@router.get(
    path="/me",
    description="Get the current user information",
    response_description="The current user information",
    response_model=UserInfo_Out,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
)
async def get_current_user_info(current_user: User_Db = Depends(get_current_user)):
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

    return UserInfo_Out(**found_user_db.dict(), organization=BasicObjectInfo(**found_organization_db.dict()))
