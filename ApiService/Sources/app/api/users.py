from fastapi import APIRouter
from fastapi import Body
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from models.users import PyObjectId, User_Db, User_In, User_Out
from passlib.context import CryptContext


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
db = client.sailDatabase

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/user", response_description="Add new users", response_model=User_Out)
async def post_user(user: User_In = Body(...)):
    user_db = jsonable_encoder(User_Db(**user.dict(), hashed_password=get_password_hash(user.password)))
    new_user = await db["users"].insert_one(user_db)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    return created_user


@router.get("/user/{id}", response_description="Get user information", response_model=User_Out)
async def get_user(id: PyObjectId):
    found_user = await db["users"].find_one({"_id": str(id)})
    return found_user
