# -------------------------------------------------------------------------------
# Engineering
# organization_helpers.py
# -------------------------------------------------------------------------------
"""Helper class for organizations"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
import random


class Organization:
    """
    Organization class
    """

    def __init__(self, name, description, avatar, admin_name, admin_job_title, admin_email, admin_password, admin_avatar):
        self.name = name
        self.description = description
        self.avatar = avatar
        self.admin_name = admin_name
        self.admin_job_title = admin_job_title
        self.admin_email = admin_email
        self.admin_password = admin_password
        self.admin_avatar = admin_avatar
        self.id = "None"

    def pretty_print(self):
        print("===Organization Data===")
        print(f"Name: {self.name}")
        print(f"Description: {self.description}")
        print(f"Avatar: {self.avatar}")
        print(f"Admin Name: {self.admin_name}")
        print(f"Admin Job Title: {self.admin_job_title}")
        print(f"Admin Email: {self.admin_email}")
        print(f"Admin Password: {self.admin_password}")
        print(f"Admin Avatar: {self.admin_avatar}")
        print(f"Org ID: {self.id}")


class User:
    """
    User class 
    """

    def __init__(self, name, email, job_title, role, avatar, password):
        self.name = name
        self.email = email
        self.job_title = job_title
        self.role = role
        self.avatar = avatar
        self.password = password
        self.id = None
