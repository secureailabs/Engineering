# -------------------------------------------------------------------------------
# Engineering
# secure_computation_nodes.py
# -------------------------------------------------------------------------------
"""APIs to manage secure computation nodes"""
import asyncio

# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
import json
import time
from ipaddress import IPv4Address
from typing import List

import aiohttp
from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

import app.utils.azure as azure
from app.api.authentication import get_current_user
from app.api.data_federations import get_existing_dataset_key
from app.api.dataset_versions import get_dataset_version
from app.data import operations as data_service
from app.log import log_message
from app.utils.background_couroutines import add_async_task
from app.utils.secrets import get_secret
from models.authentication import TokenData
from models.common import BasicObjectInfo, PyObjectId
from models.secure_computation_nodes import (
    GetMultipleSecureComputationNode_Out,
    GetSecureComputationNode_Out,
    RegisterSecureComputationNode_In,
    RegisterSecureComputationNode_Out,
    SecureComputationNode_Db,
    SecureComputationNodeInitializationVector,
    SecureComputationNodeSize,
    SecureComputationNodeState,
    SecureComputationNodeType,
    SmartBrokerInitializationVector,
    SmartBrokerScnInfo,
    UpdateSecureComputationNode_In,
)

DB_COLLECTION_SECURE_COMPUTATION_NODE = "secure-computation-node"

router = APIRouter()


########################################################################################################################
async def register_secure_computation_node(
    secure_computation_node_req: RegisterSecureComputationNode_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
) -> RegisterSecureComputationNode_Out:
    """
    Register a secure computation node

    :param secure_computation_node_req: Secure computation node request body
    :type secure_computation_node_req: RegisterSecureComputationNode_In, optional
    :param current_user: Current user information
    :type current_user: TokenData, optional
    :return: Secure computation node information
    :rtype: RegisterSecureComputationNode_Out
    """
    # Add the secure computation node to the database
    secure_computation_node_db = SecureComputationNode_Db(
        **secure_computation_node_req.dict(),
        researcher_user_id=current_user.id,
        state=SecureComputationNodeState.REQUESTED,
        researcher_id=current_user.organization_id,
        data_owner_id=PyObjectId(empty=True),
    )
    if secure_computation_node_req.type == SecureComputationNodeType.SCN:
        # Check if the digital contract and dataset exist
        dataset_version_db = await get_dataset_version(secure_computation_node_req.dataset_version_id, current_user)
        if not dataset_version_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset Version not found")

        # Set the dataowner id in the secure computation node
        secure_computation_node_db.data_owner_id = dataset_version_db.organization.id

        # Get the encryption key of the dataset
        dataset_key = await get_existing_dataset_key(
            data_federation_id=secure_computation_node_db.data_federation_id,
            dataset_id=secure_computation_node_db.dataset_id,
            current_user=current_user,
        )
        # Start the provisioning of the secure computation node in a background thread which will update the IP address
        add_async_task(provision_secure_computation_node(secure_computation_node_db, dataset_key.dataset_key))
    elif secure_computation_node_req.type == SecureComputationNodeType.SMART_BROKER:
        add_async_task(provision_smart_broker(secure_computation_node_db))
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid secure computation node type")

    await data_service.insert_one(DB_COLLECTION_SECURE_COMPUTATION_NODE, jsonable_encoder(secure_computation_node_db))

    message = f"[Register Secure Computation Node]: user_id:{current_user.id}, SCN_id: {secure_computation_node_db.id}"
    await log_message(message)

    return RegisterSecureComputationNode_Out(**secure_computation_node_db.dict())


########################################################################################################################
@router.get(
    path="/secure-computation-node",
    description="Get list of all the secure_computation_node for the current user and federation provision",
    response_description="List of secure_computation_nodes",
    response_model=GetMultipleSecureComputationNode_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_all_secure_computation_nodes(
    data_federation_provision_id: PyObjectId,
    current_user: TokenData = Depends(get_current_user),
) -> GetMultipleSecureComputationNode_Out:
    from app.api.data_federations import get_data_federation

    query = {
        "researcher_id": str(current_user.organization_id),
        "researcher_user_id": str(current_user.id),
        "data_federation_provision_id": str(data_federation_provision_id),
    }
    secure_computation_nodes = await data_service.find_by_query(DB_COLLECTION_SECURE_COMPUTATION_NODE, query)

    response_secure_computation_nodes: List[GetSecureComputationNode_Out] = []

    # Get the basic information of the data federation
    if secure_computation_nodes:
        secure_computation_node = SecureComputationNode_Db(**secure_computation_nodes[0])
        data_federation = await get_data_federation(secure_computation_node.data_federation_id, current_user)

        # Add the organization information to the data federation
        data_researcher_basic_info = [
            organization
            for organization in data_federation.research_organizations
            if organization.id == current_user.organization_id
        ][0]

        for secure_computation_node in secure_computation_nodes:
            secure_computation_node = SecureComputationNode_Db(**secure_computation_node)

            # Skip if it is a smart broker
            if secure_computation_node.type == SecureComputationNodeType.SMART_BROKER:
                continue

            dataset_basic_info = [
                dataset for dataset in data_federation.datasets if dataset.id == secure_computation_node.dataset_id
            ][0]

            # Get the basic information of the data version
            dataset_version_basic_info = await get_dataset_version(
                secure_computation_node.dataset_version_id, current_user
            )

            response_secure_computation_node = GetSecureComputationNode_Out(
                **secure_computation_node.dict(),
                data_federation=BasicObjectInfo(_id=data_federation.id, name=data_federation.name),
                dataset=dataset_basic_info,
                dataset_version=BasicObjectInfo(
                    _id=dataset_version_basic_info.id, name=dataset_version_basic_info.name
                ),
                data_owner=dataset_version_basic_info.organization,
                researcher=data_researcher_basic_info,
                researcher_user=current_user.id,
            )
            response_secure_computation_nodes.append(response_secure_computation_node)

    message = f"[Get All Secure Computation Nodes]: user_id:{current_user.id}"
    await log_message(message)

    return GetMultipleSecureComputationNode_Out(secure_computation_nodes=response_secure_computation_nodes)


########################################################################################################################
@router.get(
    path="/secure-computation-node/{secure_computation_node_id}",
    description="Get the information about a secure computation node",
    response_model=GetSecureComputationNode_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_secure_computation_node(
    secure_computation_node_id: PyObjectId, current_user: TokenData = Depends(get_current_user)
):
    from app.api.data_federations import get_data_federation

    query = {
        "researcher_id": str(current_user.organization_id),
        "_id": str(secure_computation_node_id),
    }
    secure_computation_node = await data_service.find_one(DB_COLLECTION_SECURE_COMPUTATION_NODE, query)
    if not secure_computation_node:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secure Computation Node not found")

    # Get the basic information of the data federation
    secure_computation_node = SecureComputationNode_Db(**secure_computation_node)
    data_federation = await get_data_federation(secure_computation_node.data_federation_id, current_user)

    # Add the organization information to the secure computation node information
    data_researcher_basic_info = [
        organization
        for organization in data_federation.research_organizations
        if organization.id == current_user.organization_id
    ][0]

    dataset_basic_info = BasicObjectInfo(_id=PyObjectId(empty=True), name="")
    dataset_version_basic_info = BasicObjectInfo(_id=PyObjectId(empty=True), name="")
    data_owner_basic_info = BasicObjectInfo(_id=PyObjectId(empty=True), name="")
    if secure_computation_node.type == SecureComputationNodeType.SCN:
        dataset_basic_info = [
            dataset for dataset in data_federation.datasets if dataset.id == secure_computation_node.dataset_id
        ][0]
        # Get the basic information of the data version
        dataset_version_basic_info = await get_dataset_version(secure_computation_node.dataset_version_id, current_user)
        data_owner_basic_info = dataset_version_basic_info.organization

    response_secure_computation_node = GetSecureComputationNode_Out(
        **secure_computation_node.dict(),
        data_federation=BasicObjectInfo(_id=data_federation.id, name=data_federation.name),
        dataset=dataset_basic_info,
        dataset_version=BasicObjectInfo(_id=dataset_version_basic_info.id, name=dataset_version_basic_info.name),
        data_owner=data_owner_basic_info,
        researcher=data_researcher_basic_info,
        researcher_user=current_user.id,
    )

    message = f"[Get Secure Computation Node]: user_id:{current_user.id}, SCN_id: {secure_computation_node_id}"
    await log_message(message)

    return response_secure_computation_node


########################################################################################################################
@router.put(
    path="/secure-computation-node/{secure_computation_node_id}",
    description="Update secure computation node information",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_secure_computation_node(
    secure_computation_node_id: PyObjectId,
    updated_secure_computation_node_info: UpdateSecureComputationNode_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
):
    # Check if the secure computation node exists
    secure_computation_node_db = await data_service.find_one(
        DB_COLLECTION_SECURE_COMPUTATION_NODE, {"_id": str(secure_computation_node_id)}
    )
    if not secure_computation_node_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secure Computation Node not found")
    secure_computation_node_db = SecureComputationNode_Db(**secure_computation_node_db)  # type: ignore

    if secure_computation_node_db.state == SecureComputationNodeState.WAITING_FOR_DATA:
        if updated_secure_computation_node_info.state == SecureComputationNodeState.READY:
            secure_computation_node_db.state = SecureComputationNodeState.READY
        elif updated_secure_computation_node_info.state == SecureComputationNodeState.IN_USE:
            secure_computation_node_db.state = SecureComputationNodeState.IN_USE
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    await data_service.update_one(
        DB_COLLECTION_SECURE_COMPUTATION_NODE,
        {"_id": str(secure_computation_node_id)},
        {"$set": jsonable_encoder(secure_computation_node_db)},
    )

    message = f"[Update Secure Computation Node]: user_id:{current_user.id}, SCN_id: {secure_computation_node_id}"
    await log_message(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################################################################################################################
async def deprovision_secure_computation_nodes(
    data_federation_provision_id: PyObjectId,
    current_user: TokenData = Depends(get_current_user),
):
    # Update the secure computation node
    await data_service.update_many(
        DB_COLLECTION_SECURE_COMPUTATION_NODE,
        {
            "data_federation_provision_id": str(data_federation_provision_id),
            "researcher_id": str(current_user.organization_id),
        },
        {"$set": {"state": "DELETING", "ipaddress": "0.0.0.0"}},
    )

    # Start a background task to deprovision the secure computation node which will update the status
    add_async_task(delete_resource_group(data_federation_provision_id, current_user))

    message = f"[Deprovision Secure Computation Nodes]: user_id:{current_user.id}, data_federation_provision_id: {data_federation_provision_id}"
    await log_message(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################################################################################################################
# TODO: these are temporary functions. They should be removed after the HANU is ready
async def provision_secure_computation_node(secure_computation_node_db: SecureComputationNode_Db, dataset_key: str):
    """
    Provision a secure computation node

    :param secure_computation_node_db: secure computation node information
    :type secure_computation_node_db: SecureComputationNode_Db
    :param dataset_key: dataset key
    :type dataset_key: str
    """
    try:
        # Provision the secure computation node
        if secure_computation_node_db.size == SecureComputationNodeSize.Standard_DC4ads_v5:
            secure_computation_node_db = await provision_virtual_machine(
                secure_computation_node_db, "securecomputationnode"
            )
        else:
            secure_computation_node_db = await provision_virtual_machine(secure_computation_node_db, "rpcrelated")

        # Create a SCN initialization vector json
        securecomputationnode_json = SecureComputationNodeInitializationVector(
            secure_computation_node_id=secure_computation_node_db.id,
            storage_account_name=get_secret("azure_storage_account_name"),
            dataset_storage_password=get_secret("azure_storage_account_password"),
            dataset_version_id=secure_computation_node_db.dataset_version_id,
            dataset_id=secure_computation_node_db.dataset_id,
            dataset_key=dataset_key,
            data_federation_id=secure_computation_node_db.data_federation_id,
            researcher_id=secure_computation_node_db.researcher_id,
            researcher_user_id=secure_computation_node_db.researcher_user_id,
            version=get_secret("version"),
        )

        with open(str(secure_computation_node_db.id), "w") as outfile:
            json.dump(jsonable_encoder(securecomputationnode_json), outfile)

        # Initilize the secure computation node
        await initialize_virtual_machine(secure_computation_node_db, "package.tar.gz")

    except Exception as exception:
        print(exception)
        # Update the database to mark the VM as FAILED
        secure_computation_node_db.state = SecureComputationNodeState.FAILED
        secure_computation_node_db.detail = str(exception)
        await data_service.update_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE,
            {"_id": str(secure_computation_node_db.id)},
            {"$set": jsonable_encoder(secure_computation_node_db)},
        )


########################################################################################################################
async def provision_smart_broker(smart_broker_node_db: SecureComputationNode_Db):
    """
    Provision a smart broker node

    :param smart_broker_node_db: smart broker node information
    :type smart_broker_node_db: SecureComputationNode_Db
    """
    try:
        # Provision the secure computation node
        smart_broker_node_db = await provision_virtual_machine(smart_broker_node_db, "smartbroker")

        # Wait for all the SCNs to be ready with a timeout of 15 minutes
        secure_computation_node_dbs = []
        start_time = time.time()
        while True:
            if time.time() - start_time > 900:
                raise Exception("Timeout waiting for SCNs to be ready")
            await asyncio.sleep(10)
            secure_computation_node_dbs = await data_service.find_by_query(
                DB_COLLECTION_SECURE_COMPUTATION_NODE,
                {"data_federation_provision_id": str(smart_broker_node_db.data_federation_provision_id), "type": "SCN"},
            )
            # Check if all the SCNs are ready/waiting for data
            if all(
                SecureComputationNode_Db(**secure_computation_node_db).state
                == SecureComputationNodeState.WAITING_FOR_DATA
                for secure_computation_node_db in secure_computation_node_dbs
            ):
                break

        # Create a list of SCNs to be sent to the smart broker
        secure_computation_nodes: List[SmartBrokerScnInfo] = []
        for secure_computation_node_db in secure_computation_node_dbs:
            secure_computation_node_db = SecureComputationNode_Db(**secure_computation_node_db)
            if secure_computation_node_db.ipaddress is None:
                raise Exception("IP address of SCN is not set")
            secure_computation_nodes.append(
                SmartBrokerScnInfo(
                    _id=secure_computation_node_db.id,
                    ip_address=secure_computation_node_db.ipaddress,
                    dataset_id=secure_computation_node_db.dataset_id,
                    dataset_version_id=secure_computation_node_db.dataset_version_id,
                )
            )

        # Create a SCN initialization vector json
        smart_broker_json = SmartBrokerInitializationVector(
            smart_broker_id=smart_broker_node_db.id,
            secure_computation_nodes=secure_computation_nodes,
            access_token="",
            researcher_id=smart_broker_node_db.researcher_id,
            researcher_user_id=smart_broker_node_db.researcher_user_id,
            data_federation_id=smart_broker_node_db.data_federation_id,
            version=get_secret("version"),
        )

        with open(str(smart_broker_node_db.id), "w") as outfile:
            json.dump(jsonable_encoder(smart_broker_json), outfile)

        # Initilize the secure computation node
        await initialize_virtual_machine(smart_broker_node_db, "smartbroker.tar.gz")

    except Exception as exception:
        print(exception)
        # Update the database to mark the VM as FAILED
        smart_broker_node_db.state = SecureComputationNodeState.FAILED
        smart_broker_node_db.detail = str(exception)
        await data_service.update_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE,
            {"_id": str(smart_broker_node_db.id)},
            {"$set": jsonable_encoder(smart_broker_node_db)},
        )


########################################################################################################################
async def provision_virtual_machine(
    virtual_machine_info_db: SecureComputationNode_Db, template_name: str
) -> SecureComputationNode_Db:
    """
    Provision a virtual machine

    :param virtual_machine_info_db: virtual machine information
    :type virtual_machine_info_db: SecureComputationNode_Db
    :param template_name: template name
    :type template_name: str
    :rtype: SecureComputationNode_Db
    """
    # Update the database to mark the VM as being created
    virtual_machine_info_db.state = SecureComputationNodeState.CREATING
    await data_service.update_one(
        DB_COLLECTION_SECURE_COMPUTATION_NODE,
        {"_id": str(virtual_machine_info_db.id)},
        {"$set": jsonable_encoder(virtual_machine_info_db)},
    )

    # The name of the resource group is same as the data federation provision id
    owner = get_secret("owner")
    resource_group_name = f"{owner}-{str(virtual_machine_info_db.data_federation_provision_id)}-scn"

    # Deploy the smart broker
    account_credentials = await azure.authenticate()
    deploy_response: azure.DeploymentResponse = await azure.deploy_module(
        account_credentials,
        resource_group_name,
        template_name,
        str(virtual_machine_info_db.id),
        jsonable_encoder(virtual_machine_info_db.size),
    )
    if deploy_response.status != "Success":
        raise Exception(deploy_response.note)

    # Update the database to mark the VM as INITIALIZING
    virtual_machine_info_db.ipaddress = IPv4Address(deploy_response.ip_address)
    virtual_machine_info_db.state = SecureComputationNodeState.INITIALIZING
    await data_service.update_one(
        DB_COLLECTION_SECURE_COMPUTATION_NODE,
        {"_id": str(virtual_machine_info_db.id)},
        {"$set": jsonable_encoder(virtual_machine_info_db)},
    )

    return virtual_machine_info_db


########################################################################################################################
async def initialize_virtual_machine(virtual_machine_info_db: SecureComputationNode_Db, package_filename: str):
    """
    Initialize a virtual machine

    :param virtual_machine_info_db: virtual machine information
    :type virtual_machine_info_db: SecureComputationNode_Db
    :param package_filename: package filename
    :type package_filename: str
    """
    # Sleeping for 1.5 minutes
    await asyncio.sleep(90)

    headers = {"accept": "application/json"}
    files = {
        "initialization_vector": open(str(virtual_machine_info_db.id), "rb"),
        "bin_package": open(package_filename, "rb"),
    }
    async with aiohttp.ClientSession() as session:
        async with session.put(
            "https://" + str(virtual_machine_info_db.ipaddress) + ":9090/initialization-data",
            headers=headers,
            data=files,
            verify_ssl=False,
        ) as resp:
            print("Upload package status: ", resp.status)

    # Update the database to mark the VM as WAITING_FOR_DATA
    virtual_machine_info_db.state = SecureComputationNodeState.WAITING_FOR_DATA
    await data_service.update_one(
        DB_COLLECTION_SECURE_COMPUTATION_NODE,
        {"_id": str(virtual_machine_info_db.id)},
        {"$set": jsonable_encoder(virtual_machine_info_db)},
    )


########################################################################################################################
async def delete_resource_group(data_federation_provision_id: PyObjectId, current_user: TokenData):
    """
    Delete a resource group

    :param data_federation_provision_id: data federation provision id
    :type data_federation_provision_id: PyObjectId
    :param current_user: current user information
    :type current_user: TokenData
    """
    try:
        # Delete the scn resource group
        owner = get_secret("owner")
        deployment_name = f"{owner}-{str(data_federation_provision_id)}-scn"

        account_credentials = await azure.authenticate()

        delete_response = await azure.delete_resouce_group(account_credentials, deployment_name)
        if delete_response.status != "Success":
            raise Exception(delete_response.note)

        # Update the secure computation node
        await data_service.update_many(
            DB_COLLECTION_SECURE_COMPUTATION_NODE,
            {
                "data_federation_provision_id": str(data_federation_provision_id),
                "researcher_id": str(current_user.organization_id),
            },
            {"$set": {"state": "DELETED"}},
        )
    except Exception as exception:
        print(exception)
        # Update the database to mark the VM as FAILED
        await data_service.update_many(
            DB_COLLECTION_SECURE_COMPUTATION_NODE,
            {
                "data_federation_provision_id": str(data_federation_provision_id),
                "researcher_id": str(current_user.organization_id),
            },
            {"$set": {"state": "DELETE_FAILED"}},
        )
