from fastapi import FastAPI
from typing import List
from fastapi import Body
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from models.datasets import Dataset_Db, GetDataset_In, GetDataset_Out, RegisterDataset_Out, RegisterDataset_In


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
db = client.sailDatabase

server = FastAPI()


@server.post("/remoteDataConnector", response_description="Add new dataset", response_model=RegisterDataset_Out)
async def register_remote_data_connector(dataset: RegisterDataset_In = Body(...)):
    current_user = dataset.Eosb.UserGuid
    dataset_db = Dataset_Db(**dataset.DatasetData.dict(), DataOwnerGuid=current_user, DatasetGuid=dataset.DatasetGuid)
    await db["datasets"].insert_one(jsonable_encoder(dataset_db))
    return dataset_db


@server.get("/remoteDataConnectors", response_description="Get all datasets", response_model=List[GetDataset_Out])
async def get_remote_data_connectors(request: GetDataset_In = Body(...)):
    fetched_datasets = await db["datasets"].find().to_list(None)
    return fetched_datasets


@server.get("/remoteDataConnector/{id}", response_description="Get dataset by id", response_model=GetDataset_Out)
async def get_remote_data_connector(id: str, request: GetDataset_In = Body(...)):
    created_dataset = await db["datasets"].find_one({"DatasetGuid": id})
    return created_dataset


@server.put("/remoteDataConnector/{id}", response_description="Get dataset by id", response_model=GetDataset_Out)
async def update_remote_data_connector(request: GetDataset_In = Body(...)):
    fetched_datasets = await db["datasets"].find().to_list(None)
    return fetched_datasets


@server.put("/remoteDataConnector/{id}/heartbeat", response_description="Get dataset by id", response_model=GetDataset_Out)
async def update_remote_data_connector_heartbeat(id: str, request: GetDataset_In = Body(...)):
    fetched_datasets = await db["datasets"].find().to_list(None)
    return fetched_datasets


@server.delete("/dataset/{id}")
async def delete_dataset(id: str, request: RegisterDataset_In = Body(...)):
    await db["datasets"].delete_one({"DatasetGuid": id})
