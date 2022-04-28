from fastapi import APIRouter, Body, Depends
from typing import List
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from models.datasets import Dataset_Db, GetDataset_Out, RegisterDataset_Out, RegisterDataset_In
from models.accounts import User_Db
from app.api.authentication import get_current_active_user


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
db = client.sailDatabase

router = APIRouter()


@router.post("/datasets", description="Add new dataset", response_model=RegisterDataset_Out)
async def register_dataset(dataset: RegisterDataset_In = Body(...), current_user: User_Db = Depends(get_current_active_user)):
    dataset_db = Dataset_Db(**dataset.DatasetData.dict(), DataOwnerGuid=str(current_user.id), DatasetGuid=dataset.DatasetGuid)
    await db["datasets"].insert_one(jsonable_encoder(dataset_db))
    return dataset_db


@router.get("/datasets", description="Get all datasets", response_model=List[GetDataset_Out])
async def get_datasets(current_user: User_Db = Depends(get_current_active_user)):
    fetched_datasets = await db["datasets"].find().to_list(None)
    return fetched_datasets


@router.get("/datasets/{id}", description="Get dataset by id", response_model=GetDataset_Out)
async def get_dataset(id: str, current_user: User_Db = Depends(get_current_active_user)):
    created_dataset = await db["datasets"].find_one({"DatasetGuid": id})
    return created_dataset


@router.delete("/datasets/{id}", description="Delete dataset")
async def delete_dataset(id: str, current_user: User_Db = Depends(get_current_active_user)):
    await db["datasets"].delete_one({"DatasetGuid": id})
