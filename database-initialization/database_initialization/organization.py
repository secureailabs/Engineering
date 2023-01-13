# -------------------------------------------------------------------------------
# database_initialization
# organization.py
# -------------------------------------------------------------------------------
"""Organization manager class to manage organizations"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

from sail_client import Client, SyncOperations
from sail_client.models import RegisterOrganizationIn


class OrganizationManager:
    def __init__(self, client: Client):
        """
        Initialize the organization manager class to register organizations and store their name to id mapping

        :param client: client from the sail_client library to make API calls
        :type client: Client
        """
        self.operations = SyncOperations(client)
        self.map_name_to_id = {}

    def create(
        self,
        name: str,
        description: str,
        admin_name: str,
        admin_job_title: str,
        admin_email: str,
        admin_password: str,
    ) -> str:
        """
        Register a new organization and store the name to id mapping

        :param name: unique name of the organization
        :type name: str
        :param description: description of the organization
        :type description: str
        :param admin_name: name of the admin of the organization
        :type admin_name: str
        :param admin_job_title: job title of the admin of the organization
        :type admin_job_title: str
        :param admin_email: email of the admin of the organization
        :type admin_email: str
        :param admin_password: password of the admin of the organization
        :type admin_password: str
        :return: id of the organization
        :rtype: str
        """
        register_organization_req = RegisterOrganizationIn(
            name=name,
            description=description,
            admin_name=admin_name,
            admin_job_title=admin_job_title,
            admin_email=admin_email,
            admin_password=admin_password,
        )
        response = self.operations.register_organization(register_organization_req)
        self.map_name_to_id[name] = response.id
        return response.id

    def get_id_by_name(self, name: str) -> str:
        """
        Get the id of an organization by its name

        :param name: name of the organization
        :type name: str
        :raises Exception: if the organization is not found
        :return: id of the organization
        :rtype: str
        """
        if name not in self.map_name_to_id:
            raise Exception(f"Organization {name} not found")

        return self.map_name_to_id[name]
