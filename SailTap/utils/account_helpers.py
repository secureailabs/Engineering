# -----------------------------------------------------------
#
# Account Management Helpers
#
# -----------------------------------------------------------
from config import SAIL_PASS

from utils.helpers import random_name


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
