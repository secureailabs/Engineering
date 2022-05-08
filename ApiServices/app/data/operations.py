import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
sail_db = client.sailDatabase


async def find_one(collection, query):
    return await sail_db[collection].find_one(query)


async def find_all(collection):
    return await sail_db[collection].find().to_list(None)


async def find_by_query(collection, query):
    return await sail_db[collection].find(query).to_list(None)


async def insert_one(collection, data):
    return await sail_db[collection].insert_one(data)


async def update_one(collection, query, data):
    return await sail_db[collection].update_one(query, data)


async def delete(collection, query):
    return await sail_db[collection].delete_one(query)
