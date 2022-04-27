from fastapi import APIRouter
from fastapi import Body
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from models.accounts import RegisterOrganization_In, RegisterOrganization_Out, Organization_db
from models.accounts import PyObjectId, User_Db, User_In
from passlib.context import CryptContext


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
db = client.sailDatabase
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/organization", response_description="Add new organization and admin user", response_model=RegisterOrganization_Out)
async def post_organization(organization: RegisterOrganization_In = Body(...)):
    organization_db: Organization_db = Organization_db(**organization.dict())
    organization = jsonable_encoder(organization_db)
    await db["organizations"].insert_one(organization)
    return organization_db


@router.post("/organization/{organization_id}/user", response_model=RegisterOrganization_Out)
async def post_user(user: User_In = Body(...)):
    user_db = jsonable_encoder(User_Db(**user.dict(), hashed_password=get_password_hash(user.password)))
    new_user = await db["users"].insert_one(user_db)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    return created_user


@router.get("/organizations", response_model=RegisterOrganization_Out)
async def get_organizations():
    organizations = await db["organizations"].find().to_list(None)
    return organizations


@router.get("/organization/{organization_id}", response_model=RegisterOrganization_Out)
async def get_organization(organization_id: PyObjectId):
    organization = await db["organizations"].find_one({"_id": organization_id})
    return organization


@router.get("/organization/{organization_id}/users", response_model=RegisterOrganization_Out)
async def get_users(organization_id: PyObjectId):
    users = await db["users"].find({"OrganizationGuid": organization_id}).to_list(None)
    return users


@router.get("/organization/{organization_id}/user/{user_id}", response_model=RegisterOrganization_Out)
async def get_user(organization_id: PyObjectId, user_id: PyObjectId):
    user = await db["users"].find_one({"_id": user_id, "OrganizationGuid": organization_id})
    return user


@router.put("/organization/{organization_id}", response_model=RegisterOrganization_Out)
async def put_organization(organization_id: PyObjectId, organization: Organization_db = Body(...)):
    await db["organizations"].update_one({"_id": organization_id}, {"$set": organization})
    return organization


@router.put("/organization/{organization_id}/user/{user_id}", response_model=RegisterOrganization_Out)
async def put_user(organization_id: PyObjectId, user_id: PyObjectId, user: User_Db = Body(...)):
    await db["users"].update_one({"_id": user_id, "OrganizationGuid": organization_id}, {"$set": user})
    return user


@router.delete("/organization/{organization_id}/user/{user_id}", response_model=RegisterOrganization_Out)
async def delete_user(organization_id: PyObjectId, user_id: PyObjectId):
    await db["users"].delete_one({"_id": user_id, "OrganizationGuid": organization_id})
    return user_id


@router.delete("/organization/{organization_id}", response_model=RegisterOrganization_Out)
async def delete_organization(organization_id: PyObjectId):
    await db["organizations"].delete_one({"_id": organization_id})
    return organization_id
