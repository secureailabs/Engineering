# -------------------------------------------------------------------------------
# Engineering
# conftest.py
# -------------------------------------------------------------------------------
"""Shared Orchestrator Fixtures"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
import json

import pytest
import sail.core
from config import API_PORTAL_HOSTNAME, RESEARCHER_EMAIL, SAFE_FUNCTION_DIRECTORY, SAIL_PASS, TEST_SAFE_FUNCTION_GUID


def pytest_addoption(parser):
    """
    Pytest addoption cmdline arguments

    :param parser:
    :type parser:
    """
    parser.addoption("--hostname", action="store", default=API_PORTAL_HOSTNAME)
    parser.addoption("--safefndir", action="store", default=SAFE_FUNCTION_DIRECTORY)
    parser.addoption("--safefnguid", action="store", default=TEST_SAFE_FUNCTION_GUID)


@pytest.fixture(autouse=True)
def get_portal_ip(pytestconfig):
    """
    Fixture to get the IP address of our platform service server

    :param pytestconfig:
    :type pytestconfig:
    :return: ip
    :rtype: string
    """
    return pytestconfig.getoption("ip")


@pytest.fixture(autouse=True)
def get_portal_port(pytestconfig):
    """
    Fixture to get the port of our platform service server

    :param pytestconfig:
    :type pytestconfig:
    :return: port
    :rtype: string
    """
    return int(pytestconfig.getoption("port"))


@pytest.fixture(autouse=True)
def get_portal_hostname(pytestconfig):
    """
    Fixture to get the hostname (if available) of our platform service server

    :param pytestconfig:
    :type pytestconfig:
    :return: hostname
    :rtype: string
    """
    return pytestconfig.getoption("hostname")


@pytest.fixture(autouse=True)
def get_safe_function_dir(pytestconfig):
    """
    Fixture to get the location on disk of safe functions to load

    :param pytestconfig:
    :type pytestconfig:
    :return: safefndir
    :rtype: string
    """
    return pytestconfig.getoption("safefndir")


@pytest.fixture(autouse=True)
def get_safe_function_guid(pytestconfig):
    """
    Fixture to get the guid of a test safe function

    :param pytestconfig:
    :type pytestconfig:
    :return: safefnguid
    :rtype: string
    """
    return pytestconfig.getoption("safefnguid")


@pytest.fixture
def orchestrator_load_safe_functions_fixture(get_safe_function_dir):
    """
    Fixture to load safe functions from

    :param get_safe_function_dir:
    :type get_safe_function_dir:
    """
    # Setup
    sail.core.load_safe_objects(get_safe_function_dir)
    yield

    # Teardown
    sail.core.exit_current_session()


@pytest.fixture
def orchestrator_fresh_session_fixture():
    """
    Fixture to ensure session not logged in
    """
    sail.core.exit_current_session()
    yield
    # Teardown
    sail.core.exit_current_session()


@pytest.fixture
def orchestrator_login_fixture(orchestrator_fresh_session_fixture, get_portal_ip, get_portal_port):
    """
    Fixture to establish a logged in session

    :param orchestrator_fresh_session_fixture:
    :type orchestrator_fresh_session_fixture:
    :param get_portal_ip:
    :type get_portal_ip:
    :param get_portal_port:
    :type get_portal_port:
    """
    sail.core.login(RESEARCHER_EMAIL, SAIL_PASS, get_portal_port, get_portal_ip)


@pytest.fixture
def orchestrator_get_dataset_guid_fixture(orchestrator_login_fixture):
    """
    Fixture to get dataset guid

    :param orchestrator_login_fixture:
    :type orchestrator_login_fixture:
    :return:
    :rtype:
    """
    all_datasets = sail.core.get_datasets()

    provision_ds = ""

    if all_datasets is not None:
        json_datasets = json.loads(all_datasets)
        provision_ds = list(json_datasets.keys())[0]

    return provision_ds


@pytest.fixture
def orchestrator_get_digital_contract_guid_fixture(orchestrator_login_fixture):
    """
    Fixture to get digital contract guid

    :param orchestrator_login_fixture:
    :type orchestrator_login_fixture:
    :return:
    :rtype:
    """
    all_digital_contracts = sail.core.get_digital_contracts()

    provision_dc = ""

    if all_digital_contracts is not None:
        json_datasets = json.loads(all_digital_contracts)
        provision_dc = list(json_datasets.keys())[0]

    return provision_dc
