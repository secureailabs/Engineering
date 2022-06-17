# -----------------------------------------------------------
#
# Generic Helpers
#
# -----------------------------------------------------------
import random
import string
import urllib.parse
from json import dumps


def pretty_print(msg=None, data=None, indent=4):
    """
    Pretty Print Human readable json format

    :param msg: Specified message, defaults to None
    :param data: Data to be formatted, defaults to None
    :param indent: Specified indentation for format, defaults to 4
    :type indent: int, optional
    """
    to_json = dumps(data, indent=indent)
    if not msg:
        print(f"\n{to_json}")
    else:
        print(f"\n{msg}\n {to_json}")


def url_encoded(encoded):
    """
    Helper function to encode url query strings

    :param encoded: [description]
    :type encoded: [type]
    :return: [description]
    :rtype: [type]
    """
    output = urllib.parse.urlencode(encoded, safe=":+/=@{}")
    return output


def get_response_values(response):
    """
    Helper function extract values from a response

    :param response:
    :type response:
    :return: response, response_json, user_eosb
    :rtype: (string, string, string)
    """
    response_json = None
    user_eosb = None
    try:
        response_json = response.json()
    except ValueError:
        response_json = None

    try:
        user_eosb = response_json.get("Eosb")
    except AttributeError:
        user_eosb = None

    return response, response_json, user_eosb


def random_name(length_of_string):
    """
    Helper function to generate a random name

    :param length_of_string:
    :type length_of_string: int
    :return: random_string
    :rtype: string
    """

    letters_and_digits = string.ascii_lowercase + string.digits
    random_string = ""
    for number in range(length_of_string):
        random_string += random.choice(letters_and_digits)
    return random_string
