# -----------------------------------------------------------
#
# SAIL Organization API test file
#
# -----------------------------------------------------------
import pytest
from assertpy.assertpy import assert_that
from cerberus import Validator
from tests.workflow_tests.api_portal.sail_portal_api import SailPortalFastApi
from tests.workflow_tests.utils.helpers import random_name
from tests.workflow_tests.utils.organization_helper import Organization, User


def debug_helper(response):
    print(f"\n----------HELLO------------")
    print(f"{response.url}")
    print(f"------------END--------------")


def print_response_values(function_name, response, response_json):
    print(f"\n\n=========={function_name}==========")
    print(f"Test Response: {response}\n")
    print(f"Test Response JSON: {response_json}\n")


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal",
    [
        "data_owner_sail_fast_api_portal",
        "researcher_sail_fast_api_portal",
    ],
)
def test_fastapi_get_valid_organization(sail_portal: SailPortalFastApi, request):
    """
    Test getting a valid organization.

    :param sail_portal: sail_portal fixture
    :type sail_portal: object
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)

    schema = {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "avatar": {
            "type": "string",
            "default": "AVATAR",
        },  # avatar variable currently NaN/Null/None. keeping for future iterations.
        "id": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    info_response, info_response_json = sail_portal.get_basic_user_info()
    org_id = info_response_json["organization"].get("id")
    test_response, test_response_json = sail_portal.get_organization_by_id(org_id)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(info_response.status_code).is_equal_to(200)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, org_id",
    [
        ("data_owner_sail_fast_api_portal", f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(12)}"),
        ("researcher_sail_fast_api_portal", f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(12)}"),
        ("data_owner_sail_fast_api_portal", f"{random_name(8)}-{random_name(8)}-{random_name(12)}"),
        ("researcher_sail_fast_api_portal", f"{random_name(8)}-{random_name(8)}-{random_name(12)}"),
        ("data_owner_sail_fast_api_portal", random_name(32)),
        ("researcher_sail_fast_api_portal", random_name(32)),
    ],
)
def test_fastapi_get_invalid_organization(sail_portal: SailPortalFastApi, org_id: str, request):
    """
    Test getting an invalid organization.

    :param sail_portal: sail_portal fixture
    :type sail_portal: object
    :param org_id: organization ID
    :type org_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = sail_portal.get_organization_by_id(org_id)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, new_org",
    [
        ("data_owner_sail_fast_api_portal", "create_valid_organization"),
        ("researcher_sail_fast_api_portal", "create_valid_organization"),
    ],
)
def test_fastapi_register_new_valid_organization(sail_portal: SailPortalFastApi, new_org: Organization, request):
    """
    Testing registering a new organization using valid parameters.

    :param sail_portal: sail_portal fixture
    :type sail_portal: object
    :param new_org: Organization object
    :type sail_portal: object
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    new_org = request.getfixturevalue(new_org)

    schema = {
        "id": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = sail_portal.register_new_organization(new_org=new_org)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(201)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, new_org",
    [
        ("data_owner_sail_fast_api_portal", "create_invalid_organization"),
        ("researcher_sail_fast_api_portal", "create_invalid_organization"),
    ],
)
def test_fastapi_register_new_invalid_organization(sail_portal: SailPortalFastApi, new_org: Organization, request):
    """
    Testing registering a new organization using invalid parameters.

    :param sail_portal: sail_portal fixture
    :type sail_portal: object
    :param new_org: Organization object
    :type sail_portal: object
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    new_org = request.getfixturevalue(new_org)
    new_org.name = None

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = sail_portal.register_new_organization(new_org=new_org)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, new_name, new_description, new_avatar",
    [
        (
            "researcher_sail_fast_api_portal",
            "Updated RESEARCHER Organization",
            "This org has been updated using valid credentials",
            random_name(16),
        ),
        (
            "data_owner_sail_fast_api_portal",
            "Updated DATA OWNER Organization",
            "This org has been updated using valid credentials",
            random_name(16),
        ),
    ],
)
def test_fastapi_update_valid_organization_valid_credentials(
    sail_portal: SailPortalFastApi, new_name: str, new_description: str, new_avatar: str, request
):
    """
    Testing updating a valid organization with valid credentials

    :param sail_portal: sail_portal fixture
    :type sail_portal: object
    :param new_org: Organization object
    :type new_org: object
    :param request:
    :type request:
    :param new_name: new organization name
    :type new_name: string
    :param new_description: new organization description
    :type new_description: string
    :param new_avatar: new organization avatar
    :type new_avatar: string
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)

    schema = {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "avatar": {
            "type": "string",
            "default": "AVATAR",
        },  # avatar variable currently NaN/Null/None. keeping for future iterations.
        "id": {"type": "string"},
    }

    validator = Validator(schema)

    _, info_response_json = sail_portal.get_basic_user_info()
    org_id = info_response_json["organization"].get("id")

    # Act
    original_response, original_response_json = sail_portal.get_organization_by_id(org_id)
    update_response = sail_portal.update_organization_info(org_id, new_name, new_description, new_avatar)

    test_response, test_response_json = sail_portal.get_organization_by_id(org_id)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(update_response.status_code).is_equal_to(204)
    assert_that(test_response_json["name"]).is_equal_to(new_name)
    assert_that(test_response_json["description"]).is_equal_to(new_description)
    assert_that(test_response_json["avatar"]).is_equal_to(new_avatar)

    # Replace values to original for consecutive tests
    update_response = sail_portal.update_organization_info(
        org_id, original_response_json["name"], original_response_json["description"], original_response_json["avatar"]
    )


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, sail_portal_target",
    [
        ("researcher_sail_fast_api_portal", "data_owner_sail_fast_api_portal"),
        ("data_owner_sail_fast_api_portal", "researcher_sail_fast_api_portal"),
    ],
)
def test_fastapi_update_valid_organization_invalid_credentials(
    sail_portal: SailPortalFastApi, sail_portal_target: SailPortalFastApi, request
):
    """
    Testing updating a valid organization with invalid credentials

    :param sail_portal: sail_portal fixture
    :type sail_portal: object
    :param sail_portal_target: sail_portal_target fixture
    :type sail_portal_target: object
    :param new_org: Organization object
    :type sail_portal: object
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)

    sail_portal_target = request.getfixturevalue(sail_portal_target)
    _, info_response_json = sail_portal_target.get_basic_user_info()
    target_org_id = info_response_json["organization"].get("id")

    schema = {
        "detail": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    original_response, original_response_json = sail_portal.get_organization_by_id(target_org_id)
    update_response = sail_portal.update_organization_info(
        target_org_id, "Invalid Credentials Name", "Invalid Credentials Description", "Invalid Avatar"
    )
    test_response, test_response_json = sail_portal.get_organization_by_id(target_org_id)

    # Assert
    is_valid = validator.validate(update_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(update_response.status_code).is_equal_to(403)
    assert_that(test_response_json["name"]).is_equal_to(original_response_json["name"])
    assert_that(test_response_json["description"]).is_equal_to(original_response_json["description"])
    assert_that(test_response_json["avatar"]).is_equal_to(original_response_json["avatar"])


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, org_id",
    [
        ("researcher_sail_fast_api_portal", f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(12)}"),
        ("data_owner_sail_fast_api_portal", f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(12)}"),
    ],
)
def test_fastapi_update_invalid_organization(sail_portal: SailPortalFastApi, org_id: str, request):
    """
    Testing updating an invalid organization

    :param sail_portal: sail_portal fixture
    :type sail_portal: object
    :param org_id: organization ID
    :type org_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    update_response = sail_portal.update_organization_info(
        org_id, "Invalid Name", "Invalid Description", "Invalid Avatar"
    )

    # Assert
    is_valid = validator.validate(update_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(update_response.status_code).is_equal_to(422)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_fast_api_portal",
        "data_owner_sail_fast_api_portal",
    ],
)
def test_fastapi_get_valid_organization_users(sail_portal: SailPortalFastApi, request):
    """
    Testing getting all users of a valid organization

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    :param admin_email: administrator email
    :type admin_email: string
    :param admin_pass: administrator password
    :type admin_pass: string
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)

    _, info_response_json = sail_portal.get_basic_user_info()
    org_id = info_response_json["organization"].get("id")

    schema = {
        "users": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = sail_portal.get_organization_users(org_id)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, org_id",
    [
        ("researcher_sail_fast_api_portal", f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(12)}"),
        ("data_owner_sail_fast_api_portal", f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(12)}"),
        ("researcher_sail_fast_api_portal", f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(12)}"),
        ("data_owner_sail_fast_api_portal", f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(12)}"),
        ("researcher_sail_fast_api_portal", f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(12)}"),
    ],
)
def test_fastapi_get_invalid_organization_users(sail_portal: SailPortalFastApi, org_id: str, request):
    """
    Testing getting all users of an invalid organization

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    :param admin_email: administrator email
    :type admin_email: string
    :param admin_pass: administrator password
    :type admin_pass: string
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = sail_portal.get_organization_users(org_id)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_fast_api_portal",
        "data_owner_sail_fast_api_portal",
    ],
)
def test_fastapi_get_organization_valid_user(sail_portal: SailPortalFastApi, request):
    """
    Testing getting a valid user from an organization.

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)

    _, info_response_json = sail_portal.get_basic_user_info()
    org_id = info_response_json["organization"].get("id")

    schema = {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "job_title": {"type": "string"},
        "role": {"type": "string"},
        "avatar": {
            "type": "string",
            "default": "AVATAR",
        },  # avatar variable currently NaN/Null/None. keeping for future iterations.
        "id": {"type": "string"},
        "organization": {
            "type": "dict",
            "schema": {
                "id": {"type": "string"},
                "name": {"type": "string"},
            },
        },
    }

    validator = Validator(schema)

    # Act
    _, org_response_json = sail_portal.get_organization_users(org_id)

    # Assert
    for user in org_response_json["users"]:
        test_response, test_response_json = sail_portal.get_organization_user_by_id(org_id, user["id"])
        is_valid = validator.validate(test_response_json)
        assert_that(is_valid, description=validator.errors).is_true()
        assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, user_id",
    [
        ("researcher_sail_fast_api_portal", random_name(32)),
        ("researcher_sail_fast_api_portal", random_name(32)),
        ("data_owner_sail_fast_api_portal", random_name(32)),
        ("data_owner_sail_fast_api_portal", random_name(32)),
    ],
)
def test_fastapi_get_organization_invalid_user(sail_portal: SailPortalFastApi, user_id: str, request):
    """
    Testing getting a valid user from an organization.  Currently gets the first user in the users list, then tries to get that user data. Can be updated to loop through the user list.

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)

    _, info_response_json = sail_portal.get_basic_user_info()
    org_id = info_response_json["organization"].get("id")

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = sail_portal.get_organization_user_by_id(org_id, user_id)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, new_user",
    [
        ("researcher_sail_fast_api_portal", "create_valid_user"),
        ("data_owner_sail_fast_api_portal", "create_valid_user"),
    ],
)
def test_fastapi_register_valid_user_to_organization(sail_portal: SailPortalFastApi, new_user: User, request):
    """
    Testing registering a new user to an organization using valid parameters.

    :param sail_portal: sail_portal fixture
    :type sail_portal: object
    :param new_user: new user object
    :type new_user: object
    :param request:
    :type request:
    """

    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    new_user = request.getfixturevalue(new_user)

    _, info_response_json = sail_portal.get_basic_user_info()
    org_id = info_response_json["organization"].get("id")

    schema = {
        "id": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = sail_portal.register_new_user_to_organization(org_id, new_user)

    _, verify_response_json = sail_portal.get_organization_users(org_id)
    users = verify_response_json["users"]

    is_found = False
    for x in users:
        if x["id"] == test_response_json["id"]:
            is_found = True

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(is_found).is_true()
    assert_that(test_response.status_code).is_equal_to(201)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, new_user",
    [
        ("researcher_sail_fast_api_portal", "create_invalid_user"),
        ("data_owner_sail_fast_api_portal", "create_invalid_user"),
    ],
)
def test_fastapi_register_invalid_user_to_organization(sail_portal: SailPortalFastApi, new_user: User, request):
    """
    Testing registering a new user to an organization using invalid parameters.

    :param sail_portal: sail_portal fixture
    :type sail_portal: object
    :param new_user: new user object
    :type new_user: object
    :param request:
    :type request:
    """

    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    new_user = request.getfixturevalue(new_user)

    _, info_response_json = sail_portal.get_basic_user_info()
    org_id = info_response_json["organization"].get("id")

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = sail_portal.register_new_user_to_organization(org_id, new_user)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, new_job_title, new_role, new_acc_state, new_avatar",
    [
        ("researcher_sail_fast_api_portal", "test_new_title", "ADMIN", "ACTIVE", "test_new_avatar"),
    ],
)
def test_fastapi_update_valid_user_valid_data(
    sail_portal: SailPortalFastApi, new_job_title: str, new_role: str, new_acc_state: str, new_avatar: str, request
):
    """
    Testing updating a valid organization user with valid data.

    :param sail_portal: sail_portal fixture
    :type sail_portal: object
    :param new_job_title: new job title
    :type new_job_title: str
    :param new_role: new role
    :type new_role: str
    :param new_acc_state: new account state
    :type new_acc_state: str
    :param new_avatar: new avatar
    :type new_avatar: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)

    schema = {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "job_title": {"type": "string"},
        "role": {"type": "string"},
        "avatar": {
            "type": "string",
            "default": "AVATAR",
        },  # avatar variable currently NaN/Null/None. keeping for future iterations.
        "id": {"type": "string"},
        "organization": {
            "type": "dict",
            "schema": {
                "id": {"type": "string"},
                "name": {"type": "string"},
            },
        },
    }

    validator = Validator(schema)

    _, info_response_json = sail_portal.get_basic_user_info()
    user_id = info_response_json["id"]
    org_id = info_response_json["organization"].get("id")

    # Act
    _, original_response_json = sail_portal.get_organization_user_by_id(org_id, user_id)

    update_response = sail_portal.update_organization_user(
        org_id, user_id, new_job_title, new_role, new_acc_state, new_avatar
    )

    _, verify_response_json = sail_portal.get_organization_user_by_id(org_id, user_id)

    # Assert
    is_valid = validator.validate(verify_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(update_response.status_code).is_equal_to(204)
    assert_that(verify_response_json["role"]).is_equal_to(new_role)
    assert_that(verify_response_json["job_title"]).is_equal_to(new_job_title)
    assert_that(verify_response_json["avatar"]).is_equal_to(new_avatar)

    # Replace values to original for consecutive tests
    update_response = sail_portal.update_organization_user(
        org_id,
        user_id,
        original_response_json["job_title"],
        original_response_json["role"],
        "ACTIVE",
        original_response_json["avatar"],
    )


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, user_id",
    [
        ("researcher_sail_fast_api_portal", random_name(32)),
        ("researcher_sail_fast_api_portal", random_name(32)),
        ("researcher_sail_fast_api_portal", random_name(32)),
    ],
)
def test_fastapi_update_invalid_user_valid_data(sail_portal: SailPortalFastApi, user_id: str, request):
    """
    Testing updating an invalid organization user with valid data.

    :param sail_portal: sail_portal fixture
    :type sail_portal: object
    :param user_id: user id
    :type user_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)

    _, info_response_json = sail_portal.get_basic_user_info()
    # user_id = info_response_json["id"]
    org_id = info_response_json["organization"].get("id")

    schema = {"error": {"type": "string"}}

    validator = Validator(schema)

    # Act
    update_response = sail_portal.update_organization_user(
        org_id, user_id, "test_new_title", "ADMIN", "ACTIVE", "test_new_avatar"
    )

    # Assert
    is_valid = validator.validate(update_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(update_response.status_code).is_equal_to(422)


# TODO: Retest/rewrite when permissioned user is available for testing
@pytest.mark.broken
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_fast_api_portal",
    ],
)
def test_fastapi_get_all_organizations(sail_portal: SailPortalFastApi, request):
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
    sail_portal = request.getfixturevalue(sail_portal)

    schema = {"access_token": {"type": "string"}, "refresh_token": {"type": "string"}, "token_type": {"type": "string"}}
    validator = Validator(schema)

    # Act
    test_response, test_response_json = sail_portal.get_all_organizations()

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)


# TODO: Rework after discussion about deletion.
@pytest.mark.broken
@pytest.mark.parametrize(
    "sail_portal, new_user",
    [
        ("researcher_sail_fast_api_portal", "create_valid_user"),
    ],
)
def test_fastapi_delete_valid_user_from_organization(sail_portal: SailPortalFastApi, new_user: User, request):
    """
    Test deleting a valid organization with valid credentials

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    new_user = request.getfixturevalue(new_user)

    _, info_response_json = sail_portal.get_basic_user_info()
    org_id = info_response_json["organization"].get("id")

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    temp_response, temp_response_json = sail_portal.register_new_user_to_organization(org_id, new_user)
    user_id = temp_response_json["id"]

    delete_response = sail_portal.delete_organization_user_by_id(org_id, user_id)

    verify_response, verify_response_json = sail_portal.get_organization_user_by_id(org_id, user_id)

    # Assert
    is_valid = validator.validate(verify_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(verify_response.status_code).is_equal_to(422)
    assert_that(delete_response.status_code).is_equal_to(204)


# TODO: Rework after discussion about deletion.
@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, user_id",
    [
        ("researcher_sail_fast_api_portal", random_name(32)),
        ("data_owner_sail_fast_api_portal", random_name(32)),
    ],
)
def test_fastapi_delete_invalid_user_from_organization(sail_portal: SailPortalFastApi, user_id: str, request):
    """
    Test deleting an invalid organization user with valid credentials

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)

    _, info_response_json = sail_portal.get_basic_user_info()
    org_id = info_response_json["organization"].get("id")

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    delete_response = sail_portal.delete_organization_user_by_id(org_id, user_id)

    # Assert
    is_valid = validator.validate(delete_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(delete_response.status_code).is_equal_to(422)
