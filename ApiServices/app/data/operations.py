# -------------------------------------------------------------------------------
# Engineering
# operations.py
# -------------------------------------------------------------------------------
"""Async operations for the database"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
sail_db = client.sailDatabase


async def find_one(collection, query):
    return await sail_db[collection].find_one(query)


async def find_all(collection) -> list:
    return await sail_db[collection].find().to_list(None)


async def find_by_query(collection, query) -> list:
    return await sail_db[collection].find(query).to_list(None)


async def insert_one(collection, data):
    return await sail_db[collection].insert_one(data)


async def update_one(collection, query, data):
    return await sail_db[collection].update_one(query, data)


async def update_many(collection, query, data):
    return await sail_db[collection].update_many(query, data)


async def delete(collection, query):
    return await sail_db[collection].delete_one(query)


async def drop():
    return await client.drop_database(sail_db)
