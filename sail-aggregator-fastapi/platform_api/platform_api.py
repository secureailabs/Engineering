import uuid
from typing import Dict
from uuid import uuid4

import requests

PORT = 8000


class ResearcherSession:
    def __init__(self, username, jwt, ip):
        self.username = username
        self.jwt = jwt
        self.ip = ip
        # Dict of federation name to information about the cluster (id, ip)
        self.provision_clusters = {}

    def get_federation_connect_string(self, federation_name: str):
        if federation_name in self.provision_clusters:
            return f'http://{self.provision_clusters[federation_name]["cluster_ip"]}:{self.provision_clusters[federation_name]["cluster_port"]}'
        raise Exception(f"Federation {federation_name} not found")


def login(user_name: str, password: str, ip: str) -> ResearcherSession:

    login_endpoint = f"https://{ip}:{PORT}/login"
    login_body = {"username": user_name, "password": password}
    login_request = requests.post(login_endpoint, login_body, verify=False)

    new_session = None

    if login_request.status_code == 200:
        new_session = ResearcherSession(user_name, login_request.json()["access_token"], ip)
    else:
        raise Exception("Failed to login")

    return new_session


def get_federations(session: ResearcherSession):

    assert session.jwt is not None

    federation_endpoint = f"https://{session.ip}:{PORT}/data-federations"
    request_headers = {"Authorization": f"Bearer {session.jwt}"}
    federation_request = requests.get(federation_endpoint, verify=False, headers=request_headers)

    if federation_request.status_code != 200:
        raise Exception("Failed to retrieve federations")

    return federation_request.json()["data_federations"]


def get_federation_datasets_by_name(session: ResearcherSession, federation_name: str):

    federations = get_federations(session)

    federation = [federation for federation in federations if federation["name"] == federation_name]

    if len(federation) != 1:
        raise Exception(f"Failed to find federation {federation_name}")

    dataset_list = [dataset["id"] for dataset in federation[0]["datasets"]]

    return dataset_list


def provision_federation_by_name(session: ResearcherSession, federation_name: str):

    federations = get_federations(session)

    federation_id = [federation["id"] for federation in federations if federation["name"] == federation_name]

    if len(federation_id) != 1:
        raise Exception(f"Failed to find federation {federation_name}")

    print(f"Id for federation is {federation_id[0]}")

    # Now that we have the ID call the API to start our provision operation
    # For now we just store a temporary identifier until we can really connect to Azure

    endpoint = f"https://{session.ip}:{PORT}/data-federations-provisions"
    request_body = {"data_federation_id": federation_id[0], "secure_computation_nodes_size": "Standard_D4s_v4"}
    request_headers = {"Authorization": f"Bearer {session.jwt}"}
    print(f"{request_body}")
    response = requests.post(endpoint, json=request_body, verify=False, headers=request_headers)

    if response.status_code != 201:
        raise Exception(f"Provision call failed: {response.status_code}")

    provision_id = response.json()["id"]
    session.provision_clusters[federation_name] = {}
    session.provision_clusters[federation_name]["provision_id"] = provision_id
    session.provision_clusters[federation_name]["broker_id"] = response.json()["smart_broker_id"]

    print(f"Provision id {provision_id}")
    print(f"Smart broker id: {response.json()['smart_broker_id']}")
    return provision_id


def connect_to_federation(session: ResearcherSession, federation_name: str):
    # Reach out to the API to get information about a provision
    broker_id = session.provision_clusters[federation_name]["broker_id"]

    return connect_to_federation_by_id(session, broker_id)


def connect_to_federation_by_id(session: ResearcherSession, broker_id: str):

    endpoint = f"https://{session.ip}:{PORT}/secure-computation-node/{broker_id}"
    request_headers = {"Authorization": f"Bearer {session.jwt}"}
    response = requests.get(endpoint, verify=False, headers=request_headers)

    if response.status_code != 200:
        raise Exception(f"Failed to get status for federation {broker_id}")

    state = response.json()["state"]

    return_dict = {}
    if state == "WAITING_FOR_DATA":

        # For now we assume we got a valid IP to a smart broker
        return_dict["ip"] = response.json()["ipaddress"]
        return_dict["port"] = "8000"
        # Try to connect to an endpoint
        test_endpoint = f"https://{return_dict['ip']}:{return_dict['port']}/docs"
        try:
            response = requests.get(test_endpoint, verify=False)
            if response.status_code != 200:
                return_dict = None
        except Exception:
            return_dict = None
    else:
        print(f"Federation is being provisioned...")
        return_dict = None

    return return_dict


def deprovision_federation_by_name(session: ResearcherSession, federation_name: str):

    provision_id = session.provision_clusters[federation_name]["provision_id"]

    print(f"Deprovision ID is {provision_id}")

    # We no longer want access to this, the provision_id can still be used
    del session.provision_clusters[federation_name]

    # Now that we have the ID call the API to start the de-provision operation
    deprovision_federation_by_id(session, provision_id)


def deprovision_federation_by_id(session: ResearcherSession, federation_id: uuid):
    endpoint = f"https://{session.ip}:{PORT}/data-federations-provisions/{federation_id}"
    request_headers = {"Authorization": f"Bearer {session.jwt}"}

    response = requests.delete(endpoint, verify=False, headers=request_headers)

    if response.status_code != 204:
        raise Exception(f"Failed to de-provision, status: {response.status_code}")
