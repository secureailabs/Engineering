from ipaddress import IPv4Address
from time import sleep
from fastapi import APIRouter, Depends, BackgroundTasks
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


@router.delete("/scn/{id}", response_description="Delete scn by id", response_model=ScnModel_Db)
async def delete_scn(background_tasks: BackgroundTasks, id: PyObjectId, current_user: UserBase = Depends(get_current_active_user)):
    scn_info = await db["scn"].find_one({"_id": str(id)})
    scn_db = ScnModel_Db(**scn_info)
    scn_db.State = ScnState.Deleting
    db["scn"].update_one({"_id": str(scn_db.id)}, {"$set": jsonable_encoder(scn_db)})
    background_tasks.add_task(deprovision_scn, scn_db)
    return scn_db


@router.post("/scn", response_description="Provision new scn", response_model=Provision_Scn_Out)
async def post_scn(background_tasks: BackgroundTasks, scn_info: Provision_Scn_In = Body(...), current_user: UserBase = Depends(get_current_active_user)):
    scn_db = ScnModel_Db(
        **scn_info.dict(),
        ResearcherIdentifier=current_user.id,
        State=ScnState.Provisioning,
        IPAddress=IPv4Address("0.0.0.0")
    )
    background_tasks.add_task(provision_scn, scn_db)
    await db["scn"].insert_one(jsonable_encoder(scn_db))
    return scn_db


def provision_scn(scn_db: ScnModel_Db):
    sleep(15)
    scn_db.State = ScnState.WaitingForData
    scn_db.IPAddress = IPv4Address("89.89.89.89")
    db["scn"].update_one({"_id": str(scn_db.id)}, {"$set": jsonable_encoder(scn_db)})


def deprovision_scn(scn_db: ScnModel_Db):
    sleep(15)
    scn_db.State = ScnState.Deleted
    scn_db.IPAddress = IPv4Address("0.0.0.0")
    db["scn"].update_one({"_id": str(scn_db.id)}, {"$set": jsonable_encoder(scn_db)})
