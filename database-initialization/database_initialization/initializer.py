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
from typing import Dict

from sail_client import AuthenticatedClient, Client, SyncAuthenticatedOperations, SyncOperations
from sail_client.models import BodyLogin, DataFederationDataFormat, RegisterDataFederationIn, RegisterUserIn, UserRole

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
        self.operations = SyncOperations(self.client)
        self.auth_operations: Dict[str, SyncAuthenticatedOperations] = {}
        self.organization_id: Dict[str, str] = {}
        self.password = "SailPassword@123"

    def user_login(self, username: str, password: str):
        """
        Login as a user and store the AuthenticatedClient in the auth_operations dict

        :param username: email of the user
        :type username: str
        :param password: password of the user
        :type password: str
        """
        operation = SyncOperations(self.client)
        login_req = BodyLogin(username=username, password=password)
        login_resp = operation.login(login_req)

        authenticated_client = AuthenticatedClient(
            base_url=self.client.base_url,
            timeout=self.client.timeout,
            raise_on_unexpected_status=self.client.raise_on_unexpected_status,
            verify_ssl=self.client.verify_ssl,
            token=login_resp.access_token,
        )
        self.auth_operations[username] = SyncAuthenticatedOperations(authenticated_client)

    def delete_database(self):
        """
        Delete/Drop the existing database and all the data
        """
        print("Deleting database")
        self.operations.drop_database()

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
                admin_password=self.password,
            )
            # Login for each organization as admin
            self.user_login(admin_user["email"], self.password)

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
                    password=self.password,
                    job_title=user["title"],
                    role=UserRole(user["role"]),
                )
                self.auth_operations[admin_user["email"]].register_user(
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

                # Register the data federation
                data_federation_req = RegisterDataFederationIn(
                    name=federation["name"],
                    description=federation["description"],
                    data_format=DataFederationDataFormat(federation["data_format"]),
                    data_model=federation["data_model_txt"],
                )
                data_federation_id = self.auth_operations[admin_user["email"]].register_data_federation(
                    json_body=data_federation_req,
                )

                # Add the data submitter to the data federation
                # for data_submitter in federation["data_submitters"]:
                #     self.auth_operations[admin_user["email"]].register_data_submitter(
                #         data_submitter_organization_id=self.org_manager.get_id_by_name(data_submitter),
                #         data_federation_id=data_federation_id.id,
                #     )

                # Add the researchers to the data federation
                for researcher in federation["researchers"]:
                    self.auth_operations[admin_user["email"]].register_researcher(
                        researcher_organization_id=self.org_manager.get_id_by_name(researcher),
                        data_federation_id=data_federation_id.id,
                    )
