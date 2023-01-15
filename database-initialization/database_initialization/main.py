# -------------------------------------------------------------------------------
# database_initialization
# main.py
# -------------------------------------------------------------------------------
"""Main entry point for the database initialization script"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

import json
import pkgutil
from typing import Optional

import typer
from sail_client import Client

from .initializer import Initializer


def initialize_database(
    hostname: str,
    configuration: Optional[str] = None,
):
    """
    Initialize the database with the provided configuration

    :param configuration: Json file containing the information that needs to comply with the format in the template, defaults to template configuration")
    :type configuration: Optional[str], optional
    :param hostname: Hostname or IP address of the api service. Should have the format http(s)://<hostname>:<port>
    :type hostname: str
    """
    if configuration is None:
        print(f"Using default template configuration")
        configuration_json = pkgutil.get_data(__name__, "template/db_init.json")
        assert configuration_json
        configuration_json = configuration_json.decode("utf-8")
        configuration_json = json.loads(configuration_json)
        use_template = True
    else:
        print(f"Using file {configuration}")
        with open(configuration) as fp:
            configuration_json = json.load(fp)
        use_template = False

    print(f"Connecting to {hostname}")
    client = Client(
        base_url=hostname,
        timeout=60,
        raise_on_unexpected_status=True,
        verify_ssl=False,
    )

    initializer = Initializer(client=client, config=configuration_json, use_template=use_template)
    initializer.delete_database()
    initializer.register_organizations()
    initializer.register_users()
    initializer.register_data_federations()


def cli_wrapper(
    configuration: Optional[str] = typer.Option(
        default=None,
        help="Path to configuration file. If not provided, the default template will be used",
    ),
    hostname: str = typer.Option(
        ...,
        help="Hostname or IP address of the api service.",
        prompt=True,
    ),
):
    """
    Initialize the database with the provided configuration

    :param configuration: Json file containing the information that needs to comply with the format in the template, defaults to template configuration")
    :type configuration: Optional[str], optional
    :param hostname: Hostname or IP address of the api service. Should have the format http(s)://<hostname>:<port>
    :type hostname: str
    """
    initialize_database(hostname=hostname, configuration=configuration)


def app():
    typer.run(cli_wrapper)


if __name__ == "__main__":
    app()
