########################################################################################################################
# @author Prawal Gangwar
# @brief Sail authentication and authorization service
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
########################################################################################################################

from time import time
from typing import List

from app.data import operations as data_service
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from models.accounts import User_Db, UserInfo_Out, UserRole
from models.authentication import LoginSuccess_Out, RefreshToken_In, TokenData
from passlib.context import CryptContext

########################################################################################################################
DB_COLLECTION_USERS = "users"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


# To be stored in a secure place like a vault or HSM
JWT_SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
REFRESH_SECRET = "52bb444a1aabb9a76792527e6605349e1cbc7fafb8624de4e0ddde4f84ad4066"

# Using password pepper or secret salt to ensure more security in the event of a hash
# leak along with salt. The adversary can reverse engineer the password if they know the
# salt and hash.
PASSWORD_PEPPER = "06ac6368872b368a8c67e41c1a8faa46e8471818cdbb442345fbb2205b9fc225"

# Authentication settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


########################################################################################################################
def get_password_hash(salt, password):
    return pwd_context.hash(salt + password + PASSWORD_PEPPER)


########################################################################################################################
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
        user_id = token_data.id
        if user_id is None:
            raise credentials_exception
    except JWTError as exception:
        raise credentials_exception
    return token_data


########################################################################################################################
class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User_Db = Depends(get_current_user)):
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
    if found_user is None:
        raise exception_authentication_failed

    found_user_db = User_Db(**found_user)
    if not pwd_context.verify(
        found_user_db.email + form_data.password + PASSWORD_PEPPER, found_user_db.hashed_password
    ):
        raise exception_authentication_failed

    token_data = TokenData(**found_user_db.dict(), exp=int((time() * 1000) + (ACCESS_TOKEN_EXPIRE_MINUTES * 60 * 1000)))

    access_token = jwt.encode(
        claims=jsonable_encoder(token_data),
        key=JWT_SECRET,
        algorithm=ALGORITHM,
    )

    refresh_token = jwt.encode(
        claims=jsonable_encoder(token_data),
        key=REFRESH_SECRET,
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
        payload = jwt.decode(refresh_token_request.refresh_token, REFRESH_SECRET, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
        user_id = token_data.id
        if user_id is None:
            raise credentials_exception

        found_user = await data_service.find_one(DB_COLLECTION_USERS, {"_id": str(user_id)})
        if found_user is None:
            raise credentials_exception

        found_user_db = User_Db(**found_user)
        token_data = TokenData(
            **found_user_db.dict(), exp=int((time() * 1000) + (ACCESS_TOKEN_EXPIRE_MINUTES * 60 * 1000))
        )

        access_token = jwt.encode(
            claims=jsonable_encoder(token_data),
            key=JWT_SECRET,
            algorithm=ALGORITHM,
        )

        refresh_token = jwt.encode(
            claims=jsonable_encoder(token_data),
            key=REFRESH_SECRET,
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
    if found_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return User_Db(**found_user)
