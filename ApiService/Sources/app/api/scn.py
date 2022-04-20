from fastapi import APIRouter, Depends
from fastapi import Body
from typing import List
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from models.common import PyObjectId
from models.scn import Provision_Scn_In, Provision_Scn_Out, ScnModel_Db, ScnState
from app.api.authentication import get_current_active_user
from models.users import UserBase


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
db = client.sailDatabase

router = APIRouter()


@router.get("/scns", response_description="Get all scns", response_model=List[ScnModel_Db])
async def get_scns(current_user: UserBase = Depends(get_current_active_user)):
    scns = await db["scn"].find().to_list(None)
    return scns


@router.get("/scn/{id}", response_description="Get scn by id", response_model=ScnModel_Db)
async def get_scn(id: PyObjectId, current_user: UserBase = Depends(get_current_active_user)):
    scn_info = await db["scn"].find_one({"_id": str(id)})
    return scn_info


@router.put("/scn/{id}")
async def put_scn(current_user: UserBase = Depends(get_current_active_user)):
    return {"ping": "pong!"}


@router.delete("/scn/{id}")
async def delete_scn(id: PyObjectId, current_user: UserBase = Depends(get_current_active_user)):
    return current_user


@router.post("/scn", response_description="Provision new scn", response_model=Provision_Scn_Out)
async def post_scn(scn_info: Provision_Scn_In = Body(...), current_user: UserBase = Depends(get_current_active_user)):
    scn_db = jsonable_encoder(
        ScnModel_Db(
            **scn_info.dict(),
            ResearcherIdentifier=current_user.id,
            State=ScnState.Provisioning
        )
    )
    new_scn = await db["scn"].insert_one(scn_db)
    return scn_db
