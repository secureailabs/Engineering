from fastapi import APIRouter, Depends
from fastapi import Body
from typing import List
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from models.users import PyObjectId, UserBase
from models.digitacontracts import RegisterDigitalContract_In, RegisterDigitalContract_Out, DigitalContract_Db
from app.api.authentication import get_current_active_user

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
db = client.sailDatabase

router = APIRouter()


@router.post("/digitalContract", response_description="Add new digitalContract", response_model=RegisterDigitalContract_Out)
async def post_digitalContract(digitalContract: RegisterDigitalContract_In = Body(...), current_user: UserBase = Depends(get_current_active_user)):
    digitalContract_db = jsonable_encoder(DigitalContract_Db(**digitalContract.dict()))
    new_digitalContract = await db["digitalContracts"].insert_one(digitalContract_db)
    created_digitalContract = await db["digitalContracts"].find_one({"_id": new_digitalContract.inserted_id})
    return created_digitalContract


@router.patch("/digitalContract/{id}/accept", response_description="Accept digitalContract")
async def accept_digitalContract(id: PyObjectId, current_user: UserBase = Depends(get_current_active_user)):
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"ping": "pong!"}


@router.patch("/digitalContract/{id}/activate", response_description="Researcher activates")
async def activate_digitalContract(id: PyObjectId, current_user: UserBase = Depends(get_current_active_user)):
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"ping": "pong!"}


@router.get("/digitalContracts", response_description="Get all digitalContracts", response_model=List[DigitalContract_Db])
async def get_digitalContracts(current_user: UserBase = Depends(get_current_active_user)):
    digitalContract = await db["digitalContracts"].find().to_list(None)
    return digitalContract


@router.get("/digitalContract/{id}", response_description="Get all digitalContracts", response_model=DigitalContract_Db)
async def get_digitalContract(id: PyObjectId, current_user: UserBase = Depends(get_current_active_user)):
    digitalContract = await db["digitalContracts"].find_one({"_id": str(id)})
    return digitalContract


@router.delete("/digitalContract/{id}")
async def delete_digitalContract(current_user: UserBase = Depends(get_current_active_user)):
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"ping": "pong!"}
