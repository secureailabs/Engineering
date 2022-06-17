# -------------------------------------------------------------------------------
# Engineering
# sync_operations.py
# -------------------------------------------------------------------------------
"""Sync operations for the database"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017/")
sail_db = client.sailDatabase


def find_one(collection, query):
    return sail_db[collection].find_one(query)


def find_all(collection):
    return sail_db[collection].find().to_list(None)


def find_by_query(collection, query):
    return sail_db[collection].find(query).to_list(None)


def insert_one(collection, data):
    return sail_db[collection].insert_one(data)


def update_one(collection, query, data):
    return sail_db[collection].update_one(query, data)


def delete(collection, query):
    return sail_db[collection].delete_one(query)
