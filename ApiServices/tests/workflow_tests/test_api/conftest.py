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
from tests.workflow_tests.api_portal.account_management_api import (
    AccountManagementApi,
    AccountManagementFastApi,
)
from tests.workflow_tests.api_portal.azure_template_managment_api import (
    AzureTemplateApi,
)
from tests.workflow_tests.api_portal.datafederation_management_api import (
    DataFederationManagementApi,
    DataFederationManagementFastApi,
)
from tests.workflow_tests.api_portal.dataset_management_api import (
    DataSetManagementApi,
    DataSetManagementFastApi,
)
from tests.workflow_tests.api_portal.datasetfamily_management_api import (
    DatasetFamilyManagementApi,
)
from tests.workflow_tests.api_portal.digital_contract_management_api import (
    DigitalContractManagementApi,
)
from tests.workflow_tests.api_portal.sail_portal_api import (
    SailPortalApi,
    SailPortalFastApi,
)
from tests.workflow_tests.api_portal.virtual_machine_api import VirtualMachineApi
from tests.workflow_tests.config import (
    API_PORTAL_IP,
    DATAOWNER_EMAIL,
    ORCHESTRATOR_PATH,
    PORT,
    RESEARCHER_EMAIL,
    SAIL_PASS,
)
from tests.workflow_tests.utils.dataset_helpers import Dataset, DatasetVersion
from tests.workflow_tests.utils.federation_helpers import DataFederation
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
    base_url = (
        f"https://{pytestconfig.getoption('ip')}:{pytestconfig.getoption('port')}"
    )
    return base_url


@pytest.fixture
def data_owner_sail_fast_api_portal(get_base_url):
    """
    Fixture for SailPortalApi with datowner session
    :return: SailPortalApi
    :rtype: class : api_portal.sail_portal_api.SailPortalApi
    """
    return SailPortalFastApi(
        base_url=get_base_url, email=DATAOWNER_EMAIL, password=SAIL_PASS
    )


@pytest.fixture
def researcher_sail_fast_api_portal(get_base_url):
    """
    Fixture for SailPortalApi with researcher session
    :return: SailPortalApi
    :rtype: class : api_portal.sail_portal_api.SailPortalApi
    """
    return SailPortalFastApi(
        base_url=get_base_url, email=RESEARCHER_EMAIL, password=SAIL_PASS
    )


@pytest.fixture
def researcher_sail_portal(get_base_url):
    """
    Fixture for SailPortalApi with researcher session
    :return: SailPortalApi
    :rtype: class : api_portal.sail_portal_api.SailPortalApi
    """
    return SailPortalApi(
        base_url=get_base_url, email=RESEARCHER_EMAIL, password=SAIL_PASS
    )


@pytest.fixture
def data_owner_sail_portal(get_base_url):
    """
    Fixture for SailPortalApi with datowner session
    :return: SailPortalApi
    :rtype: class : api_portal.sail_portal_api.SailPortalApi
    """
    return SailPortalApi(
        base_url=get_base_url, email=DATAOWNER_EMAIL, password=SAIL_PASS
    )


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
def dataset_management_fast_api(get_base_url):
    """
    Fixture for DataSetManagementApi
    :return: DataSetManagementApi
    :rtype: class : api_portal.dataset_management_api.DataSetManagementApi
    """
    return DataSetManagementFastApi(base_url=get_base_url)


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
def datafederation_management_fast_api(get_base_url):
    """
    Fixture for DataFederationManagementApi
    :return: DataFederationManagementApi
    :rtype: class : api_portal.datafederation_management.DataFederationManagementApi
    """
    return DataFederationManagementFastApi(base_url=get_base_url)


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
    """
    Fixture to create a valid organization for /organization endpoint testing.

    :return: new_org
    :rtype: Organization
    """
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
    """
    Fixture to create an invalid organization for /organization endpoint testing.

    :return: invalid_org
    :rtype: Organization
    """
    invalid_org = Organization(
        name=None,
        description=None,
        avatar=None,
        admin_name=None,
        admin_job_title=None,
        admin_email=None,
        admin_password=None,
        admin_avatar=None,
    )

    return invalid_org


@pytest.fixture
def create_valid_user():
    """
    Fixture to create a valid user for /organization endpoint testing.

    :return: new_user
    :rtype: User
    """
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
    """
    Fixture to create an invalid user for /organization endpoint testing.

    :return: invalid_user
    :rtype: User
    """
    invalid_user = User(
        name=None, email=None, job_title=None, role=None, avatar=None, password=None
    )

    return invalid_user


@pytest.fixture
def create_valid_dataset_csv():
    """
    Fixture to create a valid dataset for /datasets endpoint testing.

    :return: new_dataset
    :rtype: Dataset
    """
    new_dataset = Dataset(
        name=f"DatasetName{random_name(4)}",
        description=f"DatasetDescription {random_name(4)}",
        tags=f"{random_name(8)} {random_name(4)} {random_name(8)}",
        format="CSV",
    )

    return new_dataset


@pytest.fixture
def create_valid_dataset_fhir():
    """
    Fixture to create a valid dataset for /datasets endpoint testing.

    :return: new_dataset
    :rtype: Dataset
    """
    new_dataset = Dataset(
        name=f"DatasetName{random_name(8)}",
        description=f"DatasetDescription{random_name(16)}",
        tags=f"{random_name(8)},{random_name(4)},{random_name(16)}",
        format="FHIR",
    )

    return new_dataset


@pytest.fixture
def create_invalid_dataset():
    """
    Fixture to create an invalid dataset for /datasets endpoint testing.

    :return: new_dataset
    :rtype: Dataset
    """
    new_dataset = Dataset(name=12345, description=None, tags=None, format=None)

    return new_dataset


@pytest.fixture
def create_valid_dataset_version():
    """
    Fixture to create a valid dataset-version for /dataset-versions endpoint testing.

    :return: new_dataset_version
    :rtype: DatasetVersion
    """
    new_dataset_version = DatasetVersion(
        dataset_id="TEMP",
        description=f"DatasetVersionDescription {random_name(8)}",
        name=f"DatasetVersionName{random_name(4)}",
        state="NOT_UPLOADED",
    )

    return new_dataset_version


@pytest.fixture
def create_invalid_dataset_version():
    """
    Fixture to create an invalid dataset-version for /dataset-versions endpoint testing.

    :return: new_dataset_version
    :rtype: DatasetVersion
    """
    new_dataset_version = DatasetVersion(
        dataset_id=12345, description=None, name=None, state=None
    )

    return new_dataset_version


@pytest.fixture
def create_valid_data_federation():
    """
    Fixture to create a valid data federation for /data-federation endpoint testing.

    :return: new_federation
    :rtype: DataFederation
    """
    new_federation = DataFederation(
        name=f"Test Federation-{random_name(4)}",
        description=f"This is a test Federation-{random_name(4)} {random_name(8)}",
        format="FHIR",
    )

    return new_federation


@pytest.fixture
def create_invalid_data_federation():
    """
    Fixture to create an invalid data federation for /data-federation endpoint testing.

    :return: new_federation
    :rtype: DataFederation
    """
    new_federation = DataFederation(
        name=None,
        description=None,
        format=None,
    )

    return new_federation
