from fastapi import APIRouter
from fastapi import Body
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from models.organization import RegisterOrganization_In, RegisterOrganization_Out, Organization_db

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
db = client.sailDatabase

router = APIRouter()


@router.post("/organization", response_description="Add new users", response_model=RegisterOrganization_Out)
async def post_user(organization: RegisterOrganization_In = Body(...)):
    organization_db: Organization_db = Organization_db(**organization.dict())
    organization = jsonable_encoder(organization_db)
    await db["organizations"].insert_one(organization)
    return organization_db
