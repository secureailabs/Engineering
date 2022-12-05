# -------------------------------------------------------------------------------
# Engineering
# conftest.py
# -------------------------------------------------------------------------------
"""Shared Global Fixtures"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
import sys

import pytest
from tests.workflow_tests.api_portal.account_management_api import AccountManagementApi, AccountManagementFastApi
from tests.workflow_tests.api_portal.azure_template_managment_api import AzureTemplateApi
from tests.workflow_tests.api_portal.datafederation_management_api import DataFederationManagementApi
from tests.workflow_tests.api_portal.dataset_management_api import DataSetManagementApi
from tests.workflow_tests.api_portal.datasetfamily_management_api import DatasetFamilyManagementApi
from tests.workflow_tests.api_portal.digital_contract_management_api import DigitalContractManagementApi
from tests.workflow_tests.api_portal.sail_portal_api import SailPortalApi, SailPortalFastApi
from tests.workflow_tests.api_portal.virtual_machine_api import VirtualMachineApi
from tests.workflow_tests.config import (
    API_PORTAL_IP,
    DATAOWNER_EMAIL,
    ORCHESTRATOR_PATH,
    PORT,
    RESEARCHER_EMAIL,
    SAIL_PASS,
)
from tests.workflow_tests.utils.helpers import random_name
from tests.workflow_tests.utils.organization_helper import Organization, User


def pytest_addoption(parser):
    """
    Pytest addoption cmdline arguments

    :param parser:
    :type parser:
    """
    parser.addoption("--ip", action="store", default=API_PORTAL_IP)
    parser.addoption("--port", action="store", default=PORT)

    sys.path.insert(0, ORCHESTRATOR_PATH)


@pytest.fixture(autouse=True)
def get_base_url(pytestconfig):
    """
    Fixture to set base_url for tests in session

    :param pytestconfig:
    :type pytestconfig:
    :return: base_url
    :rtype: string
    """
    base_url = f"https://{pytestconfig.getoption('ip')}:{pytestconfig.getoption('port')}"
    return base_url


@pytest.fixture
def data_owner_sail_fast_api_portal(get_base_url):
    """
    Fixture for SailPortalApi with datowner session

    :return: SailPortalApi
    :rtype: class : api_portal.sail_portal_api.SailPortalApi
    """
    return SailPortalFastApi(base_url=get_base_url, email=DATAOWNER_EMAIL, password=SAIL_PASS)


@pytest.fixture
def researcher_sail_fast_api_portal(get_base_url):
    """
    Fixture for SailPortalApi with researcher session

    :return: SailPortalApi
    :rtype: class : api_portal.sail_portal_api.SailPortalApi
    """
    return SailPortalFastApi(base_url=get_base_url, email=RESEARCHER_EMAIL, password=SAIL_PASS)


@pytest.fixture
def researcher_sail_portal(get_base_url):
    """
    Fixture for SailPortalApi with researcher session

    :return: SailPortalApi
    :rtype: class : api_portal.sail_portal_api.SailPortalApi
    """
    return SailPortalApi(base_url=get_base_url, email=RESEARCHER_EMAIL, password=SAIL_PASS)


@pytest.fixture
def data_owner_sail_portal(get_base_url):
    """
    Fixture for SailPortalApi with datowner session

    :return: SailPortalApi
    :rtype: class : api_portal.sail_portal_api.SailPortalApi
    """
    return SailPortalApi(base_url=get_base_url, email=DATAOWNER_EMAIL, password=SAIL_PASS)


@pytest.fixture
def account_management_fast_api(get_base_url):
    """
    Fixture for AccountManagementApi

    :return: AccountManagementApi
    :rtype: class : api_portal.account_management_api.AccountManagementApi
    """
    return AccountManagementFastApi(base_url=get_base_url)


@pytest.fixture
def account_management(get_base_url):
    """
    Fixture for AccountManagementApi

    :return: AccountManagementApi
    :rtype: class : api_portal.account_management_api.AccountManagementApi
    """
    return AccountManagementApi(base_url=get_base_url)


@pytest.fixture
def dataset_management(get_base_url):
    """
    Fixture for DataSetManagementApi

    :return: DataSetManagementApi
    :rtype: class : api_portal.dataset_management_api.DataSetManagementApi
    """
    return DataSetManagementApi(base_url=get_base_url)


@pytest.fixture
def digitalcontract_management(get_base_url):
    """
    Fixture for DigitalContractManagementApi

    :return: DigitalContractManagementApi
    :rtype: class : api_portal.digital_contract_management_api.DigitalContractManagementApi
    """
    return DigitalContractManagementApi(base_url=get_base_url)


@pytest.fixture
def azuretemplate_management(get_base_url):
    """
    Fixture for DigitalContractManagementApi

    :return: DigitalContractManagementApi
    :rtype: class : api_portal.digital_contract_management_api.DigitalContractManagementApi
    """
    return AzureTemplateApi(base_url=get_base_url)


@pytest.fixture
def datasetfamily_management(get_base_url):
    """
    Fixture for DatasetFamilyManagementApi

    :return: DatasetFamilyManagementApi
    :rtype: class : api_portal.datasetfamily_management_api.DatasetFamilyManagementApi
    """
    return DatasetFamilyManagementApi(base_url=get_base_url)


@pytest.fixture
def datafederation_management(get_base_url):
    """
    Fixture for DataFederationManagementApi

    :return: DataFederationManagementApi
    :rtype: class : api_portal.datafederation_management.DataFederationManagementApi
    """
    return DataFederationManagementApi(base_url=get_base_url)


@pytest.fixture
def virtualmachine_management(get_base_url):
    """
    [summary]

    :param get_base_url: [description]
    :type get_base_url: [type]
    :return: [description]
    :rtype: [type]
    """
    return VirtualMachineApi(base_url=get_base_url)


@pytest.fixture
def create_valid_organization():
    new_org = Organization(
        name=f"Test Org {random_name(8)}",
        description=f"Description {random_name(16)}",
        avatar=f"Avatar{random_name(8)}",
        admin_name=f"admin{random_name(4)}",
        admin_job_title=f"admintitle{random_name(4)}",
        admin_email=f"{random_name(4)}@{random_name(4)}.com",
        admin_password="password1",
        admin_avatar=f"adminavatar{random_name(4)}",
    )

    return new_org


@pytest.fixture
def create_invalid_organization():
    new_org = Organization(
        name=None,
        description=None,
        avatar=None,
        admin_name=None,
        admin_job_title=None,
        admin_email=None,
        admin_password=None,
        admin_avatar=None,
    )

    return new_org


@pytest.fixture
def create_valid_user():
    new_user = User(
        name=f"Name{random_name(8)}",
        email=f"{random_name(4)}@{random_name(4)}.com",
        job_title=f"title{random_name(4)}",
        role="ADMIN",
        avatar=f"avatar{random_name(8)}",
        password="password1",
    )

    return new_user


@pytest.fixture
def create_invalid_user():
    new_user = User(name=None, email=None, job_title=None, role=None, avatar=None, password=None)

    return new_user
