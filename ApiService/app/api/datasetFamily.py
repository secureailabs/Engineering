from fastapi import APIRouter, Body, Depends
from typing import List
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from models.datasetFamily import DatasetFamily_Db, RegisterDatasetFamily_In, GetDatasetFamily_Out, RegisterDatasetFamily_Out, UpdateDatasetFamily_In
from models.accounts import User_Db
from app.api.authentication import get_current_active_user


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
db = client.sailDatabase

router = APIRouter()


@router.post("/datasetFamilies", description="Add a new dataset family", response_model=RegisterDatasetFamily_Out)
async def register_datasetFamily(dataset: RegisterDatasetFamily_In = Body(...), current_user: User_Db = Depends(get_current_active_user)):
    dataset_db = DatasetFamily_Db(**dataset.dict())
    await db["datasets"].insert_one(jsonable_encoder(dataset_db))
    return dataset_db


@router.get("/datasetFamilies", description="Get all dataset family", response_model=List[GetDatasetFamily_Out])
async def get_all_datasetFamily(current_user: User_Db = Depends(get_current_active_user)):
    fetched_datasets = await db["datasets"].find().to_list(None)
    return fetched_datasets


@router.get("/datasetFamilies/{id}", description="Get dataset family by id", response_model=GetDatasetFamily_Out)
async def get_datasetFamily(id: str, current_user: User_Db = Depends(get_current_active_user)):
    created_dataset = await db["datasets"].find_one({"DatasetGuid": id})
    return created_dataset


@router.put("/datasetFamilies/{id}", description="Update dataset family")
async def update_datasets(request: UpdateDatasetFamily_In = Body(...), current_user: User_Db = Depends(get_current_active_user)):
    fetched_datasets = await db["datasets"].find().to_list(None)
    return fetched_datasets


@router.delete("/datasetFamilies/{id}", description="Delete dataset family")
async def delete_dataset(id: str, current_user: User_Db = Depends(get_current_active_user)):
    await db["datasets"].delete_one({"DatasetGuid": id})
