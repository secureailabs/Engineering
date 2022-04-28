from typing import List
from fastapi import APIRouter, Depends, Body
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from models.accounts import GetOrganizations_Out, GetUsers_Out, RegisterOrganization_In, Organization_db, RegisterOrganization_Out, RegisterUser_In, RegisterUser_Out, UpdateOrganization_In, UpdateUser_In
from models.accounts import PyObjectId, User_Db
from passlib.context import CryptContext
from app.api.authentication import get_current_active_user


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
db = client.sailDatabase
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/organizations", description="Register new organization and admin user", response_model=RegisterOrganization_Out)
async def register_organization(organization: RegisterOrganization_In = Body(...)):
    organization_db: Organization_db = Organization_db(**organization.dict())
    await db["organizations"].insert_one(jsonable_encoder(organization_db))
    return organization_db


@router.post("/organizations/{organization_id}/users", description="Add new user to organization", response_model=RegisterUser_Out)
async def register_user(organization_id: PyObjectId, user: RegisterUser_In = Body(...), current_user: User_Db = Depends(get_current_active_user)):
    user_db = jsonable_encoder(User_Db(**user.dict(), hashed_password=get_password_hash(user.password)))
    new_user = await db["users"].insert_one(user_db)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    return created_user


@router.get("/organizations", description="Get list of all the organizations", response_model=List[GetOrganizations_Out])
async def get_all_organizations(current_user: User_Db = Depends(get_current_active_user)):
    organizations = await db["organizations"].find().to_list(None)
    return organizations


@router.get("/organizations/{organization_id}", description="Get the information about a organization", response_model=GetOrganizations_Out)
async def get_organization(organization_id: PyObjectId, current_user: User_Db = Depends(get_current_active_user)):
    organization = await db["organizations"].find_one({"_id": organization_id})
    return organization


@router.get("/organizations/{organization_id}/users", description="Get all users in the organization", response_model=List[GetUsers_Out])
async def get_users(organization_id: PyObjectId, current_user: User_Db = Depends(get_current_active_user)):
    users = await db["users"].find({"OrganizationGuid": organization_id}).to_list(None)
    return users


@router.get("/organizations/{organization_id}/users/{user_id}", description="Get information about a user", response_model=GetUsers_Out)
async def get_user(organization_id: PyObjectId, user_id: PyObjectId, current_user: User_Db = Depends(get_current_active_user)):
    user = await db["users"].find_one({"_id": user_id, "OrganizationGuid": organization_id})
    return user


@router.put("/organizations/{organization_id}", description="Update organization")
async def update_organization(organization_id: PyObjectId, organization: UpdateOrganization_In = Body(...), current_user: User_Db = Depends(get_current_active_user)):
    await db["organizations"].update_one({"_id": organization_id}, {"$set": organization})
    return organization


@router.put("/organizations/{organization_id}/users/{user_id}", description="Update user information")
async def update_user(organization_id: PyObjectId, user_id: PyObjectId, user: UpdateUser_In = Body(...), current_user: User_Db = Depends(get_current_active_user)):
    await db["users"].update_one({"_id": user_id, "OrganizationGuid": organization_id}, {"$set": user})
    return user


@router.delete("/organizations/{organization_id}/users/{user_id}", description="Delete user")
async def delete_user(organization_id: PyObjectId, user_id: PyObjectId, current_user: User_Db = Depends(get_current_active_user)):
    await db["users"].delete_one({"_id": user_id, "OrganizationGuid": organization_id})


@router.delete("/organizations/{organization_id}", description="Delete organization")
async def delete_organization(organization_id: PyObjectId, current_user: User_Db = Depends(get_current_active_user)):
    await db["organizations"].delete_one({"_id": organization_id})
