# -------------------------------------------------------------------------------
# Engineering
# job_test.py
# -------------------------------------------------------------------------------
"""Orchestrator Job Api Tests"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

import datetime
import json

import pytest
import sail.core
from assertpy.assertpy import assert_that
from cerberus import Validator


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_load_safe_functions_fixture")
@pytest.mark.usefixtures("orchestrator_login_fixture")
def test_run_valid_guid(get_safe_function_guid):
    """
    Test running a job with a valid guid

    :param get_safe_function_guid: fixture
    :type get_safe_function_guid: string
    """
    # Arrange
    schema = {
        "return_value": {
            "type": "string",
            "regex": r"{4[89AB][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
        }
    }
    validator = Validator(schema)

    # Act
    test_response = sail.core.run_job(get_safe_function_guid)

    # Assert
    assert_that(test_response).is_not_none()
    validate_response = {}
    validate_response["return_value"] = test_response
    is_valid = validator.validate(validate_response)
    assert_that(is_valid, description=validator.errors).is_true()


@pytest.mark.active
@pytest.mark.parametrize(
    "bad_safe_function_guid",
    [
        "{4BFBB651-2AC4-4D5A-BB74-D38838DE4722}",
        "",
        "{40FBB651-2AC4-4D5A-BB74-D38838DE4721}",
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
@pytest.mark.usefixtures("orchestrator_load_safe_functions_fixture")
def test_run_bad_guid(bad_safe_function_guid):
    """
    Test running a job with an invalid guid

    :param bad_safe_function_guid: string
    :type bad_safe_function_guid: string
    """
    # Act
    test_response = sail.core.run_job(bad_safe_function_guid)

    # Assert
    assert_that(test_response).is_none()


@pytest.mark.active
def test_job_status_no_job():
    """
    Test getting the status of a job with an invalid job ID
    """
    # Act
    test_response = sail.core.get_job_status("{48B4A25C-C030-4774-926F-15FB301C878D}")

    # Assert
    assert_that(test_response).is_equal_to("Job not found")


@pytest.mark.active
@pytest.mark.parametrize(
    "bad_job_parameter",
    [
        "{4BFBB651-2AC4-4D5A-BB74-D38838DE47}",
        "",
        "{40FBB651-2AC4-4D5A-BB74-D38838DE4721}",
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
def test_job_status_bad_parameters(bad_job_parameter):
    """
    Test getting the status of a job with an invalid job ID

    :param bad_job_parameter:
    :type bad_job_parameter:
    """
    # Act
    test_response = sail.core.get_job_status(bad_job_parameter)

    # Assert
    assert_that(test_response).is_equal_to("Job not found")


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_load_safe_functions_fixture")
@pytest.mark.usefixtures("orchestrator_login_fixture")
def test_job_status_waiting_on_parameters(get_safe_function_guid):
    """
    Test verifies job status when missing input Parameters

    :param get_safe_function_guid:
    :type get_safe_function_guid:
    """
    # Arrange
    job_id = sail.core.run_job(get_safe_function_guid)

    # Act
    test_response = sail.core.get_job_status(job_id)

    # Assert
    assert_that(test_response).is_equal_to("Missing Input Parameters")


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_load_safe_functions_fixture")
@pytest.mark.usefixtures("orchestrator_login_fixture")
def test_same_safe_function_twice(get_safe_function_guid):
    """
    Test running a job twice, we should get unique identifiers

    :param get_safe_function_guid: fixture
    :type get_safe_function_guid: string
    """
    # Arrange
    first_response = sail.core.run_job(get_safe_function_guid)

    # Act
    test_response = sail.core.run_job(get_safe_function_guid)

    # Assert
    assert_that(test_response).is_not_none()
    assert_that(test_response).is_not_equal_to(first_response)


@pytest.mark.active
def test_setting_parameter_job_not_created():
    """
    Test setting a parameter before running a job
    """

    # Act
    test_response = sail.core.set_parameter(
        "{48B4A25C-C030-4774-926F-15FB301C878D}",
        "4C21EDF165AB4EF68853FA05FB805A03",
        "1d2d543a-8c5d-49ef-95e9-4a8108bd1996",
    )

    # Assert
    assert_that(test_response).is_none()


@pytest.mark.active
@pytest.mark.parametrize(
    "user_parameter",
    [1234, 1800.90, "hello world", [1, 1, 2, 3, 5, 8, 13], {"test": 18, "value": False}, {}, [], None, False, True],
)
def test_pushing_user_parameter(user_parameter):
    """
    Test user can push values

    :param user_parameter: user defined values
    :type user_parameter:
    """
    # Arrange
    schema = {
        "return_value": {
            "type": "string",
            "regex": r"{5[4567][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
        }
    }
    validator = Validator(schema)

    # Act
    test_response = sail.core.push_user_data(user_parameter)

    # Assert
    assert_that(test_response).is_not_none()


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_load_safe_functions_fixture")
@pytest.mark.usefixtures("orchestrator_login_fixture")
def test_setting_valid_parameter(get_safe_function_guid):
    """
    Test validating valid user defined params

    :param get_safe_function_guid:
    :type get_safe_function_guid:
    """
    # Arrange
    job_id = sail.core.run_job(get_safe_function_guid)
    safe_functions = json.loads(sail.core.get_safe_functions())

    safe_function = safe_functions[get_safe_function_guid]
    input_parameter = safe_function["InputParameters"]["0"]["Uuid"]
    pushed_parameter = sail.core.push_user_data(12)

    schema = {
        "return_value": {
            "type": "string",
            "regex": r"{4[89AB][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}.{4[CDEF][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
        }
    }
    validator = Validator(schema)

    # Act
    test_response = sail.core.set_parameter(job_id, input_parameter, pushed_parameter)

    # Assert
    assert_that(test_response).is_not_none()
    print(test_response)
    validate_response = {}
    validate_response["return_value"] = test_response
    is_valid = validator.validate(validate_response)
    assert_that(is_valid, description=validator.errors).is_true()


@pytest.mark.active
@pytest.mark.parametrize("timeout_in_ms", [1000, 2000, 500, 10, 1, 0])
def test_wait_for_data_time(timeout_in_ms):
    """
    Test await for data time works as intended

    :param timeout_in_ms:
    :type timeout_in_ms:
    """
    # Arrange
    start_time = datetime.datetime.now()
    sail.core.wait_for_data(timeout_in_ms)
    end_time = datetime.datetime.now()

    # Act
    test_time = end_time - start_time

    # Assert
    test_time_in_milliseconds = (test_time.seconds * 1000) + (test_time.microseconds / 1000)
    assert_that(test_time_in_milliseconds).is_greater_than(timeout_in_ms)

    # Time wil be slightly longer than timeout
    assert_that(test_time_in_milliseconds).is_less_than(timeout_in_ms + 1)


@pytest.mark.active
def test_wait_for_data_no_job():
    """
    Test wait for data when no job
    """
    # Act
    test_response = sail.core.wait_for_data(0)

    # Assert
    assert_that(test_response).is_none()
