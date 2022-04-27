from fastapi import APIRouter
from fastapi import Body
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from models.accounts import RegisterOrganization_In, RegisterOrganization_Out, Organization_db
from models.common import PyObjectId

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
db = client.sailDatabase

router = APIRouter()


@router.post("/dataFederation", response_description="Add new organization and admin user", response_model=RegisterOrganization_Out)
async def register_data_federation(dataFederation: RegisterOrganization_In = Body(...)):
    organization_db: Organization_db = Organization_db(**dataFederation.dict())
    organization = jsonable_encoder(organization_db)
    await db["dataFederation"].insert_one(organization)
    return organization_db


@router.get("/dataFederations", response_model=RegisterOrganization_Out)
async def get_data_federations():
    dataFederations = await db["dataFederation"].find().to_list(None)
    return dataFederations


@router.get("/dataFederation/{data_federation_id}", response_model=RegisterOrganization_Out)
async def get_data_federation(data_federation_id: PyObjectId):
    dataFederation = await db["dataFederation"].find_one({"_id": data_federation_id})
    return dataFederation


@router.delete("/dataFederation/{data_federation_id}", response_model=RegisterOrganization_Out)
async def delete_data_federation(data_federation_id: PyObjectId):
    dataFederation = await db["dataFederation"].delete_one({"_id": data_federation_id})
    return dataFederation
