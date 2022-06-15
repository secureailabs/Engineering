# -----------------------------------------------------------
#
# Orchestrator Unit test file - Safe functions
#
# -----------------------------------------------------------

import json

import pytest
import sail.core
from assertpy.assertpy import assert_that
from cerberus import Validator


@pytest.mark.active
def test_list_no_loaded():
    """
    Test listing safe functions with nothing loaded
    """
    # Act
    test_response = sail.core.get_safe_functions()

    # Assert
    assert_that(test_response).is_none()


@pytest.mark.active
@pytest.mark.parametrize(
    "bad_dir_path",
    [
        "/NOT/EVEN/A/DIR",
        "$PATH",
        '".',
        "{}",
        "$SOME_VAR",
        "@($PATH)",
        "\\",
        "\rtest",
        "\nbaaaad",
        "\b",
        "\\bad_folder",
        "is space breaking?",
        "\r\b\n\b\b\b\b\b\r\r\r\r\r\r\r\r\r\r\r\r\r\r",
    ],
)
def test_load_bad_directory(bad_dir_path):
    """
    Test loading safe functions with a bad path

    :param bad_dir_path: fixture
    :type bad_dir_path: string
    """
    # Act
    test_response = sail.core.load_safe_objects(bad_dir_path)

    # Assert
    assert_that(test_response).is_equal_to(-1)


@pytest.mark.active
def test_load_no_safe_functions():
    """
    Test loading a directory with no safe functions
    """
    # Act
    test_response = sail.core.load_safe_objects(".")

    # Assert
    assert_that(test_response).is_equal_to(0)


@pytest.mark.active
def test_load_safe_functions(get_safe_function_dir):
    """
    Test loading safe functions with a good path

    :param get_safe_function_dir: fixture
    :type get_safe_function_dir: string
    """
    # Act
    test_response = sail.core.load_safe_objects(get_safe_function_dir)

    # Assert
    assert_that(test_response).is_equal_to(5)


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_load_safe_functions_fixture")
def test_list_safe_functions():
    """
    Test listing safe functions with a good path

    :param orchestrator_load_safe_functions_fixture: fixture
    :type get_safe_function_dir: None
    """
    # Arrange
    schema = {
        "return_value": {
            "type": "dict",
            "valueschema": {
                "type": "dict",
                "schema": {
                    "InputParameters": {"type": "dict"},
                    "OutputParameters": {"type": "dict"},
                    "Description": {"type": "string"},
                    "Libraries": {"type": "dict"},
                    "Title": {"type": "string"},
                    "Payload": {"type": "string"},
                    "Uuid": {"type": "string"},
                },
            },
            "keysrules": {
                "type": "string",
                "regex": r"{4[4567][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
            },
        }
    }
    validator = Validator(schema)

    # Act
    test_response = sail.core.get_safe_functions()

    # Assert
    assert_that(test_response).is_not_none()
    json_response = {}
    json_response["return_value"] = json.loads(test_response)
    is_valid = validator.validate(json_response)
    assert_that(is_valid, description=validator.errors).is_true()
