# -------------------------------------------------------------------------------
# database_initialization
# initializer.py
# -------------------------------------------------------------------------------
"""Initializzer class to initialize the database"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

import pkgutil
from pydoc import cli
from typing import Dict

from sail_client import AuthenticatedClient, Client
from sail_client.api.default import (
    drop_database,
    login,
    register_data_federation,
    register_data_submitter,
    register_researcher,
    register_user,
)
from sail_client.models import (
    BodyLogin,
    DataFederationDataFormat,
    LoginSuccessOut,
    RegisterDataFederationIn,
    RegisterDataFederationOut,
    RegisterUserIn,
    UserRole,
)

from .data_model import DataModelManager
from .organization import OrganizationManager


class Initializer:
    def __init__(self, client: Client, config: dict, use_template: bool):
        """
        Initialize the initializer class

        :param client: client from the sail_client library to make API calls
        :type client: Client
        :param config: configuration json dict to initialize the database
        :type config: dict
        :param use_template: whether to use the default template or not
        :type use_template: bool
        """
        self.client = client
        self.config = config
        self.use_template = use_template
        self.org_manager = OrganizationManager(client=client)
        self.auth_operations: Dict[str, AuthenticatedClient] = {}
        self.organization_id: Dict[str, str] = {}

    def user_login(self, username: str, password: str):
        """
        Login as a user and store the AuthenticatedClient in the auth_operations dict

        :param username: email of the user
        :type username: str
        :param password: password of the user
        :type password: str
        """
        login_req = BodyLogin(username=username, password=password)
        login_resp = login.sync(client=self.client, form_data=login_req)
        assert type(login_resp) == LoginSuccessOut

        self.auth_operations[username] = AuthenticatedClient(
            base_url=self.client.base_url,
            timeout=self.client.timeout,
            raise_on_unexpected_status=self.client.raise_on_unexpected_status,
            verify_ssl=self.client.verify_ssl,
            token=login_resp.access_token,
            follow_redirects=self.client.follow_redirects,
        )

    def delete_database(self):
        """
        Delete/Drop the existing database and all the data
        """
        print("Deleting database")
        drop_database.sync_detailed(client=self.client)

    def register_organizations(self):
        """
        Register organizations and login as admin for each organization
        """
        print("Registering organizations")
        for organization in self.config["organizations"]:
            admin_user = organization["admin"]
            self.org_manager.create(
                name=organization["name"],
                description=organization["description"],
                admin_name=organization["name"],
                admin_job_title=admin_user["title"],
                admin_email=admin_user["email"],
                admin_password=admin_user["password"],
            )
            # Login for each organization as admin
            self.user_login(admin_user["email"], admin_user["password"])

    def register_users(self):
        """
        Register users for each organization
        """
        print("Registering users")
        for organization in self.config["organizations"]:
            admin_user = organization["admin"]
            if "users" not in organization:
                continue
            for user in organization["users"]:
                register_user_req = RegisterUserIn(
                    name=user["name"],
                    email=user["email"],
                    password=user["password"],
                    job_title=user["title"],
                    role=UserRole(user["role"]),
                )
                register_user.sync(
                    client=self.auth_operations[admin_user["email"]],
                    organization_id=self.org_manager.get_id_by_name(organization["name"]),
                    json_body=register_user_req,
                )

    def register_data_federations(self):
        """
        Register data federations for each organization and add respective data submitters and researchers
        """
        print("Registering data federations")
        for organization in self.config["organizations"]:
            admin_user = organization["admin"]
            if "data_federations" not in organization:
                continue
            for federation in organization["data_federations"]:
                # Read the data model from the file
                if self.use_template:
                    federation["data_model_txt"] = pkgutil.get_data(__name__, f"template/{federation['data_model']}")
                    assert federation["data_model_txt"]
                    federation["data_model_txt"] = federation["data_model_txt"].decode("utf-8")
                else:
                    with open(federation["data_model"]) as fp:
                        federation["data_model_txt"] = fp.read()

                data_model_manager = DataModelManager(
                    federation["data_model_txt"], self.auth_operations[admin_user["email"]]
                )
                data_model_id = data_model_manager.register_data_model()

                # Register the data federation
                data_federation_req = RegisterDataFederationIn(
                    name=federation["name"],
                    description=federation["description"],
                    data_format=DataFederationDataFormat(federation["data_format"]),
                    data_model_id=data_model_id,
                )
                data_federation_id = register_data_federation.sync(
                    client=self.auth_operations[admin_user["email"]],
                    json_body=data_federation_req,
                )
                assert type(data_federation_id) == RegisterDataFederationOut

                # Add the data submitter to the data federation
                for data_submitter in federation["data_submitters"]:
                    register_data_submitter.sync(
                        client=self.auth_operations[admin_user["email"]],
                        data_submitter_organization_id=self.org_manager.get_id_by_name(data_submitter),
                        data_federation_id=data_federation_id.id,
                    )

                # Add the researchers to the data federation
                for researcher in federation["researchers"]:
                    register_researcher.sync(
                        client=self.auth_operations[admin_user["email"]],
                        researcher_organization_id=self.org_manager.get_id_by_name(researcher),
                        data_federation_id=data_federation_id.id,
                    )
