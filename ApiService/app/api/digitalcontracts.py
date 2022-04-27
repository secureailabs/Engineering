from fastapi import APIRouter, Depends
from fastapi import Body
from typing import List
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from models.accounts import PyObjectId, User_Db
from models.digitacontracts import AcceptDigitalContract_In, GetDigitalContract_Out, RegisterDigitalContract_In, RegisterDigitalContract_Out, DigitalContract_Db, DigitalContractState
from app.api.authentication import get_current_active_user

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
db = client.sailDatabase
router = APIRouter()


@router.post("/digitalContracts", description="Add new digitalContract", response_model=RegisterDigitalContract_Out)
async def post_digitalContract(digitalContract: RegisterDigitalContract_In = Body(...), current_user: User_Db = Depends(get_current_active_user)):
    dataset = await db["datasets"].find_one({"_id": str(digitalContract.DatasetIdentifier)})
    digitalContract_db = jsonable_encoder(
        DigitalContract_Db(
            **digitalContract.dict(),
            DataOwnerIdenfier=PyObjectId(dataset['dataOwnerUser']),
            ResearcherIdentifier=current_user.id,
            State=DigitalContractState.New
        )
    )
    new_digitalContract = await db["digitalContracts"].insert_one(digitalContract_db)
    created_digitalContract = await db["digitalContracts"].find_one({"_id": new_digitalContract.inserted_id})
    return created_digitalContract


@router.put("/digitalContracts/{id}/accept", description="Accept digitalContract")
async def accept_digitalContract(id: PyObjectId, current_user: User_Db = Depends(get_current_active_user), accept_params: AcceptDigitalContract_In = Body(...)):
    digitalContract = await db["digitalContracts"].find_one({"_id": str(id)})
    # if digitalContract.State != DigitalContractState.New:
    #     raise Exception("DigitalContract is not in state New")
    digitalContract["State"] = DigitalContractState.Accepted
    await db["digitalContracts"].update_one({"_id": str(id)}, {"$set": jsonable_encoder(digitalContract)})


@router.patch("/digitalContracts/{id}/activate", description="Researcher activates")
async def activate_digitalContract(id: PyObjectId, current_user: User_Db = Depends(get_current_active_user)):
    digitalContract = await db["digitalContracts"].find_one({"_id": str(id)})
    # if digitalContract.State != DigitalContractState.New:
    #     raise Exception("DigitalContract is not in state New")
    digitalContract["State"] = DigitalContractState.Activated
    await db["digitalContracts"].update_one({"_id": str(id)}, {"$set": jsonable_encoder(digitalContract)})


@router.get("/digitalContracts", description="Get all digitalContracts", response_model=List[GetDigitalContract_Out])
async def get_digitalContracts(current_user: User_Db = Depends(get_current_active_user)):
    digitalContract = await db["digitalContracts"].find().to_list(None)
    return digitalContract


@router.get("/digitalContracts/{id}", description="Get all digitalContracts", response_model=GetDigitalContract_Out)
async def get_digitalContract(id: PyObjectId, current_user: User_Db = Depends(get_current_active_user)):
    digitalContract = await db["digitalContracts"].find_one({"_id": str(id)})
    return digitalContract


@router.delete("/digitalContracts/{id}", description="Delete digitalContract")
async def delete_digitalContract(current_user: User_Db = Depends(get_current_active_user)):
    return {"ping": "pong!"}
