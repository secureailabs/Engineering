from fastapi import APIRouter, Depends
from typing import List
from fastapi import Body
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from models.datasets import Dataset_Db, RegisterDataset_Out, RegisterDataset_In
from models.users import PyObjectId, UserBase
from app.api.authentication import get_current_active_user


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
db = client.sailDatabase

router = APIRouter()


@router.post("/dataset", response_description="Add new dataset", response_model=RegisterDataset_Out)
async def post_dataset(dataset: RegisterDataset_In = Body(...), current_user: UserBase = Depends(get_current_active_user)):
    dataset_db = Dataset_Db(**dataset.dict(), dataOwnerUser=current_user.id)
    await db["datasets"].insert_one(jsonable_encoder(dataset_db))
    return dataset_db


@router.get("/datasets", response_description="Get all datasets", response_model=List[Dataset_Db])
async def get_datasets(current_user: UserBase = Depends(get_current_active_user)):
    created_dataset = await db["datasets"].find().to_list(None)
    return created_dataset


@router.get("/dataset/{id}")
async def get_dataset(id: PyObjectId, current_user: UserBase = Depends(get_current_active_user)):
    created_dataset = await db["datasets"].find_one({"_id": str(id)})
    return created_dataset


@router.delete("/dataset/{id}")
async def delete_dataset(current_user: UserBase = Depends(get_current_active_user)):
    return {"ping": "pong!"}
