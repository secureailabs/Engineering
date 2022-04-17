from fastapi import APIRouter
from fastapi import Body, status
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.users import ScnModel

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
db = client.sailDatabase

router = APIRouter()


@router.get("/scns")
async def get_scns():
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"ping": "pong!"}


@router.get("/scn/{id}")
async def get_scn():
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"ping": "pong!"}


@router.put("/scn/{id}")
async def put_scn():
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"ping": "pong!"}


@router.delete("/scn/{id}")
async def delete_scn():
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"ping": "pong!"}


@router.post("/scn", response_description="Add new scn", response_model=ScnModel)
async def post_scn(student: ScnModel = Body(...)):
    student = jsonable_encoder(student)
    new_student = await db["students"].insert_one(student)
    created_student = await db["students"].find_one({"_id": new_student.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)
