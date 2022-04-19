from fastapi import APIRouter, Depends
from fastapi import Body, status
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.scn import ScnModel
from app.api.authentication import get_current_active_user
from models.users import UserBase


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
db = client.sailDatabase

router = APIRouter()


@router.get("/scns")
async def get_scns(current_user: UserBase = Depends(get_current_active_user)):
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"ping": "pong!"}


@router.get("/scn/{id}")
async def get_scn(current_user: UserBase = Depends(get_current_active_user)):
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"ping": "pong!"}


@router.put("/scn/{id}")
async def put_scn(current_user: UserBase = Depends(get_current_active_user)):
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"ping": "pong!"}


@router.delete("/scn/{id}")
async def delete_scn(current_user: UserBase = Depends(get_current_active_user)):
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return current_user


@router.post("/scn", response_description="Add new scn", response_model=ScnModel)
async def post_scn(student: ScnModel = Body(...), current_user: UserBase = Depends(get_current_active_user)):
    student = jsonable_encoder(student)
    new_student = await db["students"].insert_one(student)
    created_student = await db["students"].find_one({"_id": new_student.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)
