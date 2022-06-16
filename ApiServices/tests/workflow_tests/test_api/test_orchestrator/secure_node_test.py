# -------------------------------------------------------------------------------
# Engineering
# secure_node_test.py
# -------------------------------------------------------------------------------
"""Orchestrator SCN Api Tests"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

import ipaddress
import json
import time

import pytest
import sail.core
from assertpy.assertpy import assert_that
from cerberus import Validator


@pytest.mark.active
@pytest.mark.parametrize(
    "bad_digital_contract",
    ["", "\r\r\r\r\r", "\b\b\b\b\b\b\b", "\t\t\t\t\t\t\t", "$PYTHON_PATH", "{146D8A80-B0DC-4E71-A2AC-C3F797E84E32}"],
)
@pytest.mark.usefixtures("orchestrator_login_fixture")
def test_provision_bad_parameters(bad_digital_contract):
    """
    Test provisioning a digital contract with bad parameters

    :param bad_digital_contract:
    :type bad_digital_contract:
    """
    # Act
    test_response = sail.core.provision_secure_computational_node(bad_digital_contract, "DS_GUID", "VM_TYPE")

    # Assert
    json_response = json.loads(test_response)
    assert_that(json_response["Status"]).is_equal_to(False)


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_login_fixture")
def test_provision_not_logged_in():
    """
    Test provisioning a digital contract without being logged in
    """
    # Arrange

    json_digital_contracts = json.loads(sail.core.get_digital_contracts())
    digital_contract_guid = list(json_digital_contracts.keys())[0]
    sail.core.exit_current_session()

    # Act
    test_response = sail.core.provision_secure_computational_node(digital_contract_guid, "DS_GUID", "VM_TYPE")

    # Assert
    json_response = json.loads(test_response)
    assert_that(json_response["Status"]).is_equal_to(False)


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_fresh_session_fixture")
def test_wait_provision_not_logged_in():
    """
    Test waiting on a digital contract provisioning when not logged in
    """

    # Act
    test_response = sail.core.wait_for_all_secure_nodes_to_be_provisioned(0)

    # Assert
    assert_that(test_response).is_none()


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_login_fixture")
def test_wait_no_provision():
    """
    Test that when we have no provisions active we don't wait
    """
    # Arrange
    start_time = time.time()
    sail.core.wait_for_all_secure_nodes_to_be_provisioned(60000)
    end_time = time.time()

    # Act
    test_duration = end_time - start_time

    # Assert
    assert_that(test_duration).is_less_than(60)


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_login_fixture")
def test_wait_return_no_provision():
    """
    Test that when we have no provisions we return what we expect
    """

    # Act
    test_response = sail.core.wait_for_all_secure_nodes_to_be_provisioned(1000)

    # Assert
    assert_that(test_response).is_not_none()
    json_response = {}
    json_response["return_value"] = json.loads(test_response)
    assert_that(json_response["return_value"]["AllDone"]).is_equal_to(True)


@pytest.mark.functional
class TestProvisionScn:
    """
    Class Test Provision SCNS marked for functional
    """

    @pytest.fixture(scope="function", autouse=True)
    def setup_teardown(self, orchestrator_get_dataset_guid_fixture, orchestrator_get_digital_contract_guid_fixture):
        """
        Setup and Teardown fixture for function inside class

        :param orchestrator_get_dataset_guid_fixture:
        :type orchestrator_get_dataset_guid_fixture:
        :param orchestrator_get_digital_contract_guid_fixture:
        :type orchestrator_get_digital_contract_guid_fixture:
        """
        print(f"\n*******SETUP for functional Orchestrator SCN Provision TEST*******\n")
        print(f"List of Digital Contracts:")
        print(f"{orchestrator_get_digital_contract_guid_fixture}")
        print(f"List of DataSets:")
        print(f"{orchestrator_get_dataset_guid_fixture}")
        yield
        print(f"\n*******TEARDOWN for functional Orchestrator SCN Provision TEST*******\n")
        # Wait for 4 minutes = 240 000 milliseconds
        print(f"Sleep for 4 min awaiting vm start and configuration!!!\n")
        sail.core.wait_for_all_secure_nodes_to_be_provisioned(240000)
        output = sail.core.deprovision_digital_contract(orchestrator_get_digital_contract_guid_fixture)
        assert_that(output).is_equal_to(1)

    def test_real_provision(
        self,
        orchestrator_get_dataset_guid_fixture,
        orchestrator_get_digital_contract_guid_fixture,
    ):
        """
        Test issuing a real provision call and waiting on it to complete successfully

        :param orchestrator_get_dataset_guid_fixture:
        :type orchestrator_get_dataset_guid_fixture:
        :param orchestrator_get_digital_contract_guid_fixture:
        :type orchestrator_get_digital_contract_guid_fixture:
        """
        # Arrange
        provision_dc = orchestrator_get_digital_contract_guid_fixture
        provision_ds = orchestrator_get_dataset_guid_fixture

        schema = {
            "SCNGuid": {
                "type": "string",
                "regex": r"{4[0123][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
            },
            "Message": {"type": "string", "required": False},
            "Status": {"type": "boolean"},
        }

        validator = Validator(schema)

        # Act
        test_response = sail.core.provision_secure_computational_node(provision_dc, provision_ds, "Standard_D8s_v4")

        # Assert
        assert_that(test_response).is_not_none()
        json_response = {}
        json_response = json.loads(test_response)
        is_valid = validator.validate(json_response)
        assert_that(is_valid, description=validator.errors).is_true()

    @pytest.mark.skip(
        reason="BOARD-1438, Skip since nightly does not have reliable way to deploy remote data connector"
    )
    def test_wait_provision(
        self,
        orchestrator_get_dataset_guid_fixture,
        orchestrator_get_digital_contract_guid_fixture,
    ):
        """
        Test issuing a real provision call and waiting on it to complete successfully

        :param orchestrator_get_dataset_guid_fixture:
        :type orchestrator_get_dataset_guid_fixture:
        :param orchestrator_get_digital_contract_guid_fixture:
        :type orchestrator_get_digital_contract_guid_fixture:
        """

        # Arrange
        provision_dc = orchestrator_get_digital_contract_guid_fixture
        provision_ds = orchestrator_get_dataset_guid_fixture

        provision_response = sail.core.provision_secure_computational_node(
            provision_dc, provision_ds, "Standard_D8s_v4"
        )

        # Act
        # Wait for 3 minutes = 240 000 milliseconds
        test_response = sail.core.wait_for_all_secure_nodes_to_be_provisioned(240000)

        # Assert
        assert_that(test_response).is_not_none()
        json_response = {}
        json_response = json.loads(test_response)
        provision_json = {}
        provision_json = json.loads(provision_response)
        assert_that(len(json_response["Succeeded"].keys())).is_equal_to(1)
        assert_that(list(json_response["Succeeded"].keys())[0]).is_equal_to(provision_json["SCNGuid"])
        assert_that(len(json_response["InProgress"].keys())).is_equal_to(0)
        assert_that(len(json_response["Failed"].keys())).is_equal_to(0)

    @pytest.mark.skip(
        reason="BOARD-1438, Skip since nightly does not have reliable way to deploy remote data connector"
    )
    @pytest.mark.usefixtures("orchestrator_load_safe_functions_fixture")
    def test_wait_assign_parameters(
        self,
        orchestrator_get_dataset_guid_fixture,
        orchestrator_get_digital_contract_guid_fixture,
        get_safe_function_guid,
    ):
        """
        Test issuing a real provision call, waiting for it to complete, add the dataset to it,
        and confirm that the job gets assigned an SCN IP Address

        :param orchestrator_get_dataset_guid_fixture:
        :type orchestrator_get_dataset_guid_fixture:
        :param orchestrator_get_digital_contract_guid_fixture:
        :type orchestrator_get_digital_contract_guid_fixture:
        :param get_safe_function_guid:
        :type get_safe_function_guid:
        """

        # Arrange
        provision_dc = orchestrator_get_digital_contract_guid_fixture
        provision_ds = orchestrator_get_dataset_guid_fixture

        sail.core.provision_secure_computational_node(provision_dc, provision_ds, "Standard_D8s_v4")

        sail.core.wait_for_all_secure_nodes_to_be_provisioned(240000)

        job_id = sail.core.run_job(get_safe_function_guid)
        safe_functions = json.loads(sail.core.get_safe_functions())
        safe_function = safe_functions[get_safe_function_guid]
        input_parameter = safe_function["InputParameters"]["0"]["Uuid"]
        sail.core.set_parameter(job_id, input_parameter, provision_ds)

        # Act
        test_response = sail.core.get_ip_for_job(job_id)

        # Assert
        assert_that(test_response).is_not_none()
        assert_that(test_response).is_not_equal_to("")
        ip_error = True
        try:
            ipaddress.ip_address(test_response)
            ip_error = False
        except Exception as e:
            ip_error = True

        assert_that(ip_error).is_equal_to(False)

    @pytest.mark.skip(
        reason="BOARD-1438, Skip since nightly does not have reliable way to deploy remote data connector"
    )
    @pytest.mark.usefixtures("orchestrator_load_safe_functions_fixture")
    def test_multiple_scns_parameters(
        self,
        orchestrator_get_dataset_guid_fixture,
        orchestrator_get_digital_contract_guid_fixture,
        get_safe_function_guid,
    ):
        """
        Test issuing a real provision call, waiting for it to complete, add the dataset to it,
        and confirm that the job gets assigned an SCN IP Address

        :param orchestrator_get_dataset_guid_fixture:
        :type orchestrator_get_dataset_guid_fixture:
        :param orchestrator_get_digital_contract_guid_fixture:
        :type orchestrator_get_digital_contract_guid_fixture:
        :param get_safe_function_guid:
        :type get_safe_function_guid:
        """

        # Arrange
        provision_dc = orchestrator_get_digital_contract_guid_fixture
        provision_ds = orchestrator_get_dataset_guid_fixture

        provision_response = []
        provision_response.append(
            sail.core.provision_secure_computational_node(provision_dc, provision_ds, "Standard_D8s_v4")
        )
        provision_response.append(
            sail.core.provision_secure_computational_node(provision_dc, provision_ds, "Standard_D8s_v4")
        )

        sail.core.wait_for_all_secure_nodes_to_be_provisioned(240000)

        job_id = []
        job_id.append(sail.core.run_job(get_safe_function_guid))
        job_id.append(sail.core.run_job(get_safe_function_guid))
        safe_functions = json.loads(sail.core.get_safe_functions())
        safe_function = safe_functions[get_safe_function_guid]
        input_parameter = safe_function["InputParameters"]["0"]["Uuid"]
        sail.core.set_parameter(job_id[0], input_parameter, provision_ds)
        sail.core.set_parameter(job_id[1], input_parameter, provision_ds)

        # Act
        test_response = []
        for job_idx in range(0, 2):
            test_response.append(sail.core.get_ip_for_job(job_id[job_idx]))

        # Assert
        for job_idx in range(0, 2):
            assert_that(test_response[job_idx]).is_not_none()
            assert_that(test_response[job_idx]).is_not_equal_to("")
            ip_error = True
            try:
                ipaddress.ip_address(test_response[job_idx])
                ip_error = False
            except Exception as e:
                ip_error = True

            assert_that(ip_error).is_equal_to(False)

        assert_that(test_response[0]).is_not_equal_to(test_response[1])
