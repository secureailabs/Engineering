from fastapi import APIRouter, Body, Depends
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from models.dataFederation import RegisterDataFederation_In, DataFederation_Db, RegisterDataFederation_Out
from models.common import PyObjectId
from app.api.authentication import get_current_active_user
from models.accounts import User_Db

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
db = client.sailDatabase

router = APIRouter()


@router.post("/dataFederations", description="Add new data federation", response_model=RegisterDataFederation_Out)
async def register_data_federation(dataFederation: RegisterDataFederation_In = Body(...), current_user: User_Db = Depends(get_current_active_user)):
    organization_db: DataFederation_Db = DataFederation_Db(**dataFederation.dict())
    organization = jsonable_encoder(organization_db)
    await db["dataFederation"].insert_one(organization)
    return organization_db


@router.get("/dataFederations", description="Get all data federations", response_model=list)
async def get_data_federations(current_user: User_Db = Depends(get_current_active_user)):
    dataFederations = await db["dataFederation"].find().to_list(None)
    return dataFederations


@router.get("/dataFederations/{data_federation_id}", description="Get data federation by id", response_model=DataFederation_Db)
async def get_data_federation(data_federation_id: PyObjectId, current_user: User_Db = Depends(get_current_active_user)):
    dataFederation = await db["dataFederation"].find_one({"_id": data_federation_id})
    return dataFederation


@router.delete("/dataFederations/{data_federation_id}", description="Delete data federation")
async def delete_data_federation(data_federation_id: PyObjectId, current_user: User_Db = Depends(get_current_active_user)):
    dataFederation = await db["dataFederation"].delete_one({"_id": data_federation_id})
    return dataFederation
