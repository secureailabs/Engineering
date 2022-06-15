# -----------------------------------------------------------
#
# SAIL API test file
#
# -----------------------------------------------------------
import threading

import pytest
from assertpy.assertpy import assert_that
from cerberus import Validator
from models.authentication import LoginSuccess_Out
from tests.workflow_tests.api_portal.sail_portal_api import SailPortalApi, SailPortalFastApi
from tests.workflow_tests.config import DATAOWNER_EMAIL, RESEARCHER_EMAIL, SAIL_PASS, TEMP_PASS


def debug_helper(response):
    print(f"\n----------HELLO------------")
    print(f"{response.url}")
    print(f"------------END--------------")


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "email, password",
    [
        (RESEARCHER_EMAIL, SAIL_PASS),
        (DATAOWNER_EMAIL, SAIL_PASS),
    ],
)
def test_fastapi_login_entry(get_base_url: str, email: str, password: str):
    """
    Testing valid credentials

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param email: email
    :type email: string
    :param password: password
    :type password: string
    """
    # Arrange
    sail_portal = SailPortalFastApi(base_url=get_base_url, email=email, password=password)
    schema = {
        "access_token": {"type": "string"},
        "refresh_token": {"type": "string"},
        "token_type": {"type": "string"},
    }

    validator = Validator(schema)
    # Act
    test_response, test_response_json = sail_portal.login_for_access_token()
    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)
    assert_that(LoginSuccess_Out(**test_response_json))


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "email, password",
    [
        (DATAOWNER_EMAIL, TEMP_PASS),
        (RESEARCHER_EMAIL, TEMP_PASS),
        ("abc@example.com", SAIL_PASS),
        ("123", SAIL_PASS),
        (SAIL_PASS, SAIL_PASS),
        (SAIL_PASS, "4321"),
    ],
)
def test_bad_fastapi_login_invalid_user_entry(get_base_url: str, email: str, password: str):
    """
    Testing invalid credentials

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param email: email
    :type email: string
    :param password: password
    :type password: string
    """

    # Arrange
    sail_portal = SailPortalFastApi(base_url=get_base_url, email=email, password=password)
    schema = {"detail": {"type": "string"}}
    validator = Validator(schema)

    # Act
    test_response, test_response_json = sail_portal.login_for_access_token()

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(401)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal",
    [
        "data_owner_sail_fast_api_portal",
        "researcher_sail_fast_api_portal",
    ],
)
def test_get_current_user_refresh_token(sail_portal, request):
    """
    Refresh the JWT token for the current logged in user

    :param sail_portal: sail_portal fixture
    :type sail_portal: object
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "access_token": {"type": "string"},
        "refresh_token": {"type": "string"},
        "token_type": {"type": "string"},
    }
    validator = Validator(schema)
    # Act
    test_response, test_response_json = sail_portal.get_refresh_token()
    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)
    assert_that(LoginSuccess_Out(**test_response_json))


# TODO BROKEN : "detail": "Operation not permitted" requires not implemented SAIL_ACTOR
@pytest.mark.broken
@pytest.mark.parametrize(
    "sail_portal",
    [
        "data_owner_sail_fast_api_portal",
        "researcher_sail_fast_api_portal",
    ],
)
def test_get_list_organizations_info(sail_portal, request):
    """
    SAIL ACTOR get list of all organizations
    :param sail_portal: _description_
    :type sail_portal: _type_
    :param request: _description_
    :type request: _type_
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "organizations": {
            "type": "dict",
            "schema": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "avatar": {"required": False, "nullable": True, "type": "string"},
                "id": {"type": "string"},
            },
        },
    }
    validator = Validator(schema)
    # Act
    test_response, test_response_json = sail_portal.get_all_organization_info()
    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)


# TODO FASTAPI Test long sessions

# * -------------------------------------------------------------- OLD API BELOW --------------------------------------------------------------
# ! -------------------------------------------------------------- OLD API BELOW --------------------------------------------------------------
# ? -------------------------------------------------------------- OLD API BELOW --------------------------------------------------------------
# ! Completed FASTAPI Conversion via test_fastapi_login_entry
@pytest.mark.active
@pytest.mark.parametrize(
    "email, password",
    [
        (RESEARCHER_EMAIL, SAIL_PASS),
        (DATAOWNER_EMAIL, SAIL_PASS),
    ],
)
def test_valid_login_entry(get_base_url: str, email: str, password: str):
    """
    Testing valid credentials

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param email: email
    :type email: string
    :param password: password
    :type password: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=email, password=password)
    schema = {"Eosb": {"type": "string"}, "Status": {"type": "number"}}
    validator = Validator(schema)
    # Act
    for x in range(10):
        login_response, login_response_json, user_eosb = sail_portal.login()
    # Assert
    is_valid = validator.validate(login_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(login_response.status_code).is_equal_to(201)


# ! Completed FASTAPI Conversion via test_bad_fastapi_login_invalid_user_entry
@pytest.mark.active
@pytest.mark.parametrize(
    "email, password",
    [
        (DATAOWNER_EMAIL, TEMP_PASS),
        (RESEARCHER_EMAIL, TEMP_PASS),
        ("abc@example.com", SAIL_PASS),
        ("123", SAIL_PASS),
        (SAIL_PASS, SAIL_PASS),
        (SAIL_PASS, "4321"),
    ],
)
def test_bad_login_invalid_user_entry(get_base_url: str, email: str, password: str):
    """
    Testing invalid credentials

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param email: email
    :type email: string
    :param password: password
    :type password: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=email, password=password)
    schema = {"Status": {"type": "number"}}
    validator = Validator(schema)

    # Act
    login_response, login_response_json, _ = sail_portal.login()

    # Assert
    is_valid = validator.validate(login_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(login_response.status_code).is_equal_to(401)


# ! Completed FASTAPI Conversion via test_get_current_user_info
@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_get_basic_user_information(sail_portal, request):
    """
    Testing get request for basic user information

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "AccessRights": {"type": "number"},
        "Email": {"type": "string"},
        "Eosb": {"type": "string"},
        "OrganizationGuid": {"type": "string"},
        "OrganizationName": {"type": "string"},
        "PhoneNumber": {"type": "string"},
        "Status": {"type": "number"},
        "Title": {"type": "string"},
        "UserGuid": {"type": "string"},
        "Username": {"type": "string"},
    }
    validator = Validator(schema)

    # Act
    test_response, test_response_json, user_eosb = sail_portal.get_basic_user_info()
    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)


# TODO TO BE CONVERTED TO FASTAPI WHEN API IN PLACE
@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal, current_password, new_password",
    [
        ("researcher_sail_portal", SAIL_PASS, TEMP_PASS),
        ("researcher_sail_portal", TEMP_PASS, SAIL_PASS),
        ("data_owner_sail_portal", SAIL_PASS, TEMP_PASS),
        ("data_owner_sail_portal", TEMP_PASS, SAIL_PASS),
    ],
)
def test_update_password(sail_portal, request, current_password: str, new_password: str):
    """
    Test password update

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param current_password: current password
    :type current_password: string
    :param new_password: new password
    :type new_password: string
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {"Eosb": {"type": "string"}, "Status": {"type": "number"}}
    validator = Validator(schema)

    # Act
    test_response, test_response_json, user_eosb = sail_portal.update_password(current_password, new_password)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)


# TODO confer with PRAWAL ON JWT CHECKS
@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_check_good_eosb(sail_portal, request):
    """
    Test checking a valid EOSB

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {"Eosb": {"type": "string"}, "Status": {"type": "number"}}
    validator = Validator(schema)

    _, _, login_eosb = sail_portal.login()

    # Act
    test_response, test_response_json, user_eosb = sail_portal.check_eosb(login_eosb)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)


# TODO confer with PRAWAL ON JWT CHECKS
@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
@pytest.mark.parametrize(
    "bad_eosb",
    [
        # An EOSB that was once valid, but now is long expired
        "5iEQAhtloSOsV0Ak6LLvTUPqpM3QACXu/KgkHQBHXV0oIIqpbbD0FRkoT\
jmV9/8bcIrCuTkDAABkMNUGiRYq07rHUnLtWaD8TZZubLhIqsH9GYMgZA\
5Q8WbPJyRGXQtmm0LIsDzWWMF/cPWMDngUCrNEfpQpQNfeH3nZVuT0oeG\
mKzsgnzeV2avXsjbAafJoinrydTkqaimcwyYr1LDcY29sZ73YhlrW5Gjb\
7zM0FBS5PV9DnaMFPpOdTSH7+JMavnSEdQZ/mnxiJ3JOXqJULUsMJr9C2\
cw+2DD/8EYmCdBuQ0Ruh1uGUFTPoqLqb29zuSjOnPFlbXz5NmIyZJxKm8\
+BrASHPqbpkYXQEIWSg3cZhcwxvc5eO0eVIt0cpOI/oicYie4Ke8FGPdj\
VMmIqu/U+FrOPbwWyHxzTZUi4PyUbyVBHfSeSxoEaFzs95zlbupTTuqJx\
SCaj7v3O3hZpIo/yKM3BMvQ9wEAV/ndjPoRe4wnmZHUCbkjJMSSZ01OlX\
pTCEXhET+0YlFERlmdNYl1zWDivfWZeVpsVCwSrg2SyBLeRvKG8jlBV30\
xwz2qHbcF5HjXoZRYnWAxfXhbLvsgu/TaLG4y55kQCuKEY+W8bCDjA4K3\
/AzSlg0TfsVTuI8YHE+JPt/bwBOYG16vCGwAODz2ZRNt0muWBYdoeGFXw\
gIib8v3iCfi2EGPipHm9HMgP3S9URuhIKck9NRmKJxY7vgMJEl/RXMrOk\
qtEqtaH9iytV/dkacnSWvISLI8HmlFCNGItbl4XEmiugj5+OvnJF7MmkP\
WxZOysKXcaFFNzFNKCe4YVNfMSCSyglpZtO3US+8+rn3Wy6uC0Yoq+C5p\
h1+4g7oohqhAU5PkPk+9FYWf4RR98sGzxGJ1R+4fJHc3j9VgyXrVKugaE\
TkDKWrOo14a/3sd6GfmW4ppv4it6nIBeue6xdllX9l93Se964kLyiyzTw\
GwBoOf0ODDl6IyTxUZpWj8P7hmujeAKOTeM9/wBBCKbu/IrKSbzCBdd+8\
J1zTGAQ9FKleJkjLxEzroOgQu+U/fobLSkWzts4zk1t5VgkY8fRgp9NFO\
jqhyoIxZPxYe3qtxWPx/oP+TVo4iGqvMKpPqcklRWqUYqsFggmv2GhHov\
bWy86x9e+RnZNL9UY7B6jXof5FbHJBCsRkYyGlaxKZESbg==",
        "hello world!",
        # An invalidly encoded EOSB (same as above but last character changed)
        "5iEQAhtloSOsV0Ak6LLvTUPqpM3QACXu/KgkHQBHXV0oIIqpbbD0FRkoT\
jmV9/8bcIrCuTkDAABkMNUGiRYq07rHUnLtWaD8TZZubLhIqsH9GYMgZA\
5Q8WbPJyRGXQtmm0LIsDzWWMF/cPWMDngUCrNEfpQpQNfeH3nZVuT0oeG\
mKzsgnzeV2avXsjbAafJoinrydTkqaimcwyYr1LDcY29sZ73YhlrW5Gjb\
7zM0FBS5PV9DnaMFPpOdTSH7+JMavnSEdQZ/mnxiJ3JOXqJULUsMJr9C2\
cw+2DD/8EYmCdBuQ0Ruh1uGUFTPoqLqb29zuSjOnPFlbXz5NmIyZJxKm8\
+BrASHPqbpkYXQEIWSg3cZhcwxvc5eO0eVIt0cpOI/oicYie4Ke8FGPdj\
VMmIqu/U+FrOPbwWyHxzTZUi4PyUbyVBHfSeSxoEaFzs95zlbupTTuqJx\
SCaj7v3O3hZpIo/yKM3BMvQ9wEAV/ndjPoRe4wnmZHUCbkjJMSSZ01OlX\
pTCEXhET+0YlFERlmdNYl1zWDivfWZeVpsVCwSrg2SyBLeRvKG8jlBV30\
xwz2qHbcF5HjXoZRYnWAxfXhbLvsgu/TaLG4y55kQCuKEY+W8bCDjA4K3\
/AzSlg0TfsVTuI8YHE+JPt/bwBOYG16vCGwAODz2ZRNt0muWBYdoeGFXw\
gIib8v3iCfi2EGPipHm9HMgP3S9URuhIKck9NRmKJxY7vgMJEl/RXMrOk\
qtEqtaH9iytV/dkacnSWvISLI8HmlFCNGItbl4XEmiugj5+OvnJF7MmkP\
WxZOysKXcaFFNzFNKCe4YVNfMSCSyglpZtO3US+8+rn3Wy6uC0Yoq+C5p\
h1+4g7oohqhAU5PkPk+9FYWf4RR98sGzxGJ1R+4fJHc3j9VgyXrVKugaE\
TkDKWrOo14a/3sd6GfmW4ppv4it6nIBeue6xdllX9l93Se964kLyiyzTw\
GwBoOf0ODDl6IyTxUZpWj8P7hmujeAKOTeM9/wBBCKbu/IrKSbzCBdd+8\
J1zTGAQ9FKleJkjLxEzroOgQu+U/fobLSkWzts4zk1t5VgkY8fRgp9NFO\
jqhyoIxZPxYe3qtxWPx/oP+TVo4iGqvMKpPqcklRWqUYqsFggmv2GhHov\
bWy86x9e+RnZNL9UY7B6jXof5FbHJBCsRkYyGlaxKZESbf==",
    ],
)
def test_check_bad_eosb(sail_portal, bad_eosb, request):
    """
    Test checking an invalid valid EOSB

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param bad_eosb: a malformed/expired EOSB
    :type bad_eosb: string
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {"Status": {"type": "number"}}
    validator = Validator(schema)

    # Act
    test_response, test_response_json, user_eosb = sail_portal.check_eosb(bad_eosb)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb).is_none()
    assert_that(test_response.status_code).is_equal_to(401)


# TODO confer with PRAWAL ON JWT CHECKS
@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_check_missing_eosb(sail_portal, request):
    """
    Test checking a missing EOSB

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    # Act
    test_response, test_response_json, user_eosb = sail_portal.check_eosb(None)

    # Assert
    assert_that(test_response_json).is_none()
    assert_that(user_eosb).is_none()
    assert_that(test_response.status_code).is_equal_to(400)


# TODO TO BE CONVERTED TO FASTAPI WHEN API IN PLACE
@pytest.mark.stress
@pytest.mark.parametrize(
    "num_threads",
    [10, 25, 50, 100, 150, 200, 500, 1000],
)
def test_get_basic_user_stress(data_owner_sail_portal, num_threads):
    """
    Run a test with many threads to query user info, and then confirm the
    API still responds

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param num_threads: parameterized value
    :type num_threads: int
    """
    # Arrange

    threads = []
    for _ in range(num_threads):
        new_thread = threading.Thread(target=data_owner_sail_portal.get_basic_user_info)
        new_thread.start()
        threads.append(new_thread)

    for thread in threads:
        thread.join()

    # Act
    test_response, _, _ = data_owner_sail_portal.get_basic_user_info()

    # Assert
    assert_that(test_response.status_code).is_equal_to(200)
