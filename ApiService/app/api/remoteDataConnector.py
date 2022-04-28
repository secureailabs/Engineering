from fastapi import APIRouter, Body, Depends
from typing import List
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from models.accounts import User_Db
from app.api.authentication import get_current_active_user
from models.remoteDataConnector import GetRemoteDataConnectors_Out, HeartbeatRemoteDataConnector_In, HeartbeatRemoteDataConnector_Out, RegisterRemoteDataConnector_In, RegisterRemoteDataConnector_Out, RemoteDataConnector_db

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
db = client.sailDatabase
router = APIRouter()


@router.post("/remoteDataConnectors", description="Register remote data connector", response_model=RegisterRemoteDataConnector_Out)
async def register_remote_data_connector(dataset: RegisterRemoteDataConnector_In = Body(...), current_user: User_Db = Depends(get_current_active_user)):
    dataset_db = RemoteDataConnector_db(**dataset.dict())
    await db["datasets"].insert_one(jsonable_encoder(dataset_db))
    return dataset_db


@router.get("/remoteDataConnectors", description="List all remote data connectors", response_model=List[GetRemoteDataConnectors_Out])
async def get_remote_data_connectors(current_user: User_Db = Depends(get_current_active_user)):
    fetched_datasets = await db["datasets"].find().to_list(None)
    return fetched_datasets


@router.get("/remoteDataConnectors/{id}", description="Get remote data connectors by id", response_model=GetRemoteDataConnectors_Out)
async def get_remote_data_connector(id: str, current_user: User_Db = Depends(get_current_active_user)):
    created_dataset = await db["datasets"].find_one({"DatasetGuid": id})
    return created_dataset


@router.put("/remoteDataConnectors/{id}", description="Update remote data connectors")
async def update_remote_data_connector(current_user: User_Db = Depends(get_current_active_user)):
    fetched_datasets = await db["datasets"].find().to_list(None)
    return fetched_datasets


@router.put("/remoteDataConnectors/{id}/heartbeat", description="remote data connectors heartbeat", response_model=HeartbeatRemoteDataConnector_Out)
async def update_remote_data_connector_heartbeat(id: str, heartbeat: HeartbeatRemoteDataConnector_In = Body(...), current_user: User_Db = Depends(get_current_active_user)):
    fetched_datasets = await db["datasets"].find().to_list(None)
    return fetched_datasets


@router.delete("/remoteDataConnectors/{id}", description="Delete remote data connectors")
async def delete_dataset(id: str, current_user: User_Db = Depends(get_current_active_user)):
    await db["datasets"].delete_one({"DatasetGuid": id})
