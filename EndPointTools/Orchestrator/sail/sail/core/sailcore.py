################################################################################
#
#
# @file sailcore.py
# @author Jingwei Zhang + David Gascon
# @date 25 Jan 2022
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
# @brief Python interop between the orchestrator DLL and python
#
################################################################################
from .. import SAILPyAPI
import getpass
import pickle, json, requests, pprint, time
import pandas
from concurrent.futures import ThreadPoolExecutor


def login(email, password, port, IP):

    if None == password:
        password = getpass.getpass(prompt="Password: ")

    return SAILPyAPI.login(email,password, port, IP)

def get_current_eosb():
    return SAILPyAPI.get_current_eosb()

def exit_current_session():
    return SAILPyAPI.exit_current_session()

def get_safe_functions():
    return SAILPyAPI.get_safe_functions()

def get_digital_contracts():
    return SAILPyAPI.get_digital_contracts()

def load_safe_objects(safe_object_dir):
    return SAILPyAPI.load_safe_objects(safe_object_dir)

def get_datasets():
    return SAILPyAPI.get_datasets()

def get_tables():
    return SAILPyAPI.get_tables()

def provision_secure_computational_node(digital_contract_guid, dataset_guid, virtual_machine_type):
    return SAILPyAPI.provision_secure_computational_node(digital_contract_guid, dataset_guid, virtual_machine_type)

def run_job(safe_object_guid):
    return SAILPyAPI.run_job(safe_object_guid)

def wait_for_all_secure_nodes_to_be_provisioned(timeout):
    return SAILPyAPI.wait_for_all_secure_nodes_to_be_provisioned(timeout)

def set_parameter(job_guid, parameter_guid, str_value):
    return SAILPyAPI.set_parameter(job_guid, parameter_guid, str_value)

def push_user_data(user_data):
    return SAILPyAPI.push_user_data(pickle.dumps(user_data))

def get_job_status(job_guid):
    return SAILPyAPI.get_job_status(job_guid)

def pull_data(output_id):
    return SAILPyAPI.pull_data(output_id)

def wait_for_data(timeout_in_milliseconds):
    return SAILPyAPI.wait_for_data(timeout_in_milliseconds)

def get_ip_for_job(job_guid):
    return SAILPyAPI.get_ip_for_job(job_guid)

def deprovision_digital_contract(digital_contract_guid):
    return SAILPyAPI.deprovision_digital_contract(digital_contract_guid)