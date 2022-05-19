"""
Pytest fixtures
"""
import sys

import pytest
from api_portal.account_management_api import AccountManagementApi
from api_portal.azure_template_managment_api import AzureTemplateApi
from api_portal.datafederation_management_api import DataFederationManagementApi
from api_portal.dataset_management_api import DataSetManagementApi
from api_portal.datasetfamily_management_api import DatasetFamilyManagementApi
from api_portal.digital_contract_management_api import DigitalContractManagementApi
from api_portal.sail_portal_api import SailPortalApi
from api_portal.virtual_machine_api import VirtualMachineApi
from config import API_PORTAL_IP, DATAOWNER_EMAIL, ORCHESTRATOR_PATH, PORT, RESEARCHER_EMAIL, SAIL_PASS


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
