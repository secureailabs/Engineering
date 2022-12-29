# -------------------------------------------------------------------------------
# Engineering
# dataset_helpers.py
# -------------------------------------------------------------------------------
"""Data Federation Helpers"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------


class DataFederation:
    """
    Data Federation Helper Class
    """

    def __init__(self, name: str, description: str, format: str):
        self.name = name
        self.description = description
        self.format = format

    def pretty_print(self):
        print(f"\n-----------------------------------------------")
        print(f"|Federation Name: {self.name}")
        print(f"|Federation Description: {self.description}")
        print(f"|Federation Format: {self.format}")
        print(f"-----------------------------------------------\n")
