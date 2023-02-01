# -------------------------------------------------------------------------------
# Engineering
# dataset_helpers.py
# -------------------------------------------------------------------------------
"""Dataset Management Helpers"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
import datetime
import uuid
from datetime import timezone

from tests.workflow_tests.utils.helpers import random_name


def get_dataset_payload():
    """
    Helper to return template for dataset payload

    :return: dataset_payload, rand_uuid, dataset_name
    :rtype: (dict, str, str)
    """
    rand_uuid = str(uuid.uuid4())
    dataset_name = random_name(10)
    # Set UTC timestamp
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    dataset_payload = {
        "DatasetGuid": f"{{{rand_uuid}}}",
        "DatasetData": {
            "VersionNumber": "0x00000001",
            "DatasetName": f"{dataset_name}",
            "Description": "For all the Oaks",
            "Keywords": "computer science, software,programming",
            "PublishDate": utc_timestamp,
            "PrivacyLevel": 1,
            "JurisdictionalLimitations": "N/A",
            "Tables": {
                "52d7aa80-f18f-4932-af61-ecf6fd74c064": {
                    "ColumnName": ",AGE,BMI,PD-L1 level before treatment,PD-L1 level after treatment,PD-L2 level before treatment,PD-L2 level after treatment,PD1 level before treatment,PD1 level after treatment,",
                    "Description": "table 1_2",
                    "Hashtags": "t1h2",
                    "Name": "1_2.csv",
                    "NumberColumns": 9,
                    "NumberRows": 300,
                },
                "59b35181-c54c-4dd2-a17d-aa37f0296a87": {
                    "ColumnName": ",AGE,on drug,condition,",
                    "Description": "table2_2.csv",
                    "Hashtags": "t2h2",
                    "Name": "2_2.csv",
                    "NumberColumns": 4,
                    "NumberRows": 400,
                },
                "68dfc6be-3f14-467a-b796-274a3da45d29": {
                    "ColumnName": ",age,postcode,salary,",
                    "Description": "table 3_2.csv",
                    "Hashtags": "t3h2",
                    "Name": "3_2.csv",
                    "NumberColumns": 4,
                    "NumberRows": 100,
                },
            },
        },
    }
    return dataset_payload, rand_uuid, dataset_name


class Dataset:
    """
    Dataset Helper Class
    """

    def __init__(self, name: str, description: str, tags: str, format: str):
        self.name = name
        self.description = description
        self.tags = tags
        self.format = format

    def pretty_print(self):
        print(f"Dataset Name: {self.name}")
        print(f"Dataset Description: {self.description}")
        print(f"Dataset tags: {self.tags}")
        print(f"Dataset Format: {self.format}")


class DatasetVersion:
    """
    Dataset Version Helper Class
    """

    def __init__(self, dataset_id: str, description: str, name: str, state: str):
        self.dataset_id = dataset_id
        self.description = description
        self.name = name
        self.state = state

    def pretty_print(self):
        print(f"Dataset-Version ID: {self.dataset_id}")
        print(f"Dataset-Version Description: {self.description}")
        print(f"Dataset-Version Name: {self.name}")
        print(f"Dataset-Version State: {self.state}")

    def set_dataset_id(self, new_dataset_id: str):
        self.dataset_id = new_dataset_id
