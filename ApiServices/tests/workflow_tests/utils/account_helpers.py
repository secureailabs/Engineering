# -------------------------------------------------------------------------------
# Engineering
# account_helpers.py
# -------------------------------------------------------------------------------
"""Account Management Helpers"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
from tests.workflow_tests.config import SAIL_PASS
from tests.workflow_tests.utils.helpers import random_name


def get_add_user_payload():
    """
    Helper function to return a add user template payload

    :return: add_user_payload, user_email
    :rtype: (dict, str)
    """
    name = random_name(5)
    add_user_payload = {
        "Email": f"{name}@test.com",
        "Password": SAIL_PASS,
        "Name": f"{name}",
        "PhoneNumber": 1231231234,
        "Title": f"{name}",
        "AccessRights": 1,
    }
    user_email = add_user_payload.get("Email")
    return add_user_payload, user_email
