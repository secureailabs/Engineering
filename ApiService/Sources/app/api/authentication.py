from fastapi import APIRouter
import motor.motor_asyncio


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
db = client.sailDatabase

router = APIRouter()


@router.get("/login")
async def login():
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"ping": "pong!"}
