# -------------------------------------------------------------------------------
# Engineering
# secure_computation_nodes.py
# -------------------------------------------------------------------------------
"""APIs to manage secure computation nodes"""
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
from uuid import uuid4

import app.utils.azure as azure
import requests
from app.api.authentication import get_current_user
from app.api.dataset_versions import get_dataset_version
from app.data import operations as data_service
from app.data import sync_operations as sync_data_service
from app.utils.secrets import get_secret
from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from models.authentication import TokenData
from models.common import BasicObjectInfo, PyObjectId
from models.secure_computation_nodes import (
    GetMultipleSecureComputationNode_Out,
    GetSecureComputationNode_Out,
    RegisterSecureComputationNode_In,
    RegisterSecureComputationNode_Out,
    SecureComputationNode_Db,
    SecureComputationNodeState,
    UpdateSecureComputationNode_In,
)

DB_COLLECTION_SECURE_COMPUTATION_NODE = "secure-computation-node"

router = APIRouter()


########################################################################################################################
async def register_secure_computation_node(
    background_tasks: BackgroundTasks,
    secure_computation_node_req: RegisterSecureComputationNode_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
) -> RegisterSecureComputationNode_Out:
    try:
        # Check if the digital contract and dataset exist
        dataset_version_db = await get_dataset_version(secure_computation_node_req.dataset_version_id, current_user)
        if not dataset_version_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset Version not found")

        # Add the secure computation node to the database
        secure_computation_node_db = SecureComputationNode_Db(
            **secure_computation_node_req.dict(),
            researcher_user_id=current_user.id,
            state=SecureComputationNodeState.REQUESTED,
            researcher_id=current_user.organization_id,
            data_owner_id=dataset_version_db.organization.id,
        )
        await data_service.insert_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE, jsonable_encoder(secure_computation_node_db)
        )

        # Start the provisioning of the secure computation node in a background thread which will update the IP address
        background_tasks.add_task(provision_virtual_machine, secure_computation_node_db)

        return RegisterSecureComputationNode_Out(**secure_computation_node_db.dict())
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


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
    try:
        from app.api.data_federations import get_data_federation

        query = {
            "researcher_id": str(current_user.id),
            "data_federation_provision_id": str(data_federation_provision_id),
        }
        secure_computation_nodes = await data_service.find_by_query(DB_COLLECTION_SECURE_COMPUTATION_NODE, query)

        response_secure_computation_nodes: List[GetSecureComputationNode_Out] = []

        # Get the basic information of the data federation
        if secure_computation_nodes:
            secure_computation_node = SecureComputationNode_Db(**secure_computation_nodes[0].dict())
            data_federation = await get_data_federation(
                secure_computation_node.data_federation_provision_id, current_user
            )

            # Add the organization information to the data federation
            data_researcher_basic_info = [
                organization
                for organization in data_federation.research_organizations
                if organization.id == current_user.organization_id
            ][0]

            for secure_computation_node in secure_computation_nodes:
                secure_computation_node = SecureComputationNode_Db(**secure_computation_node.dict())

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

        return GetMultipleSecureComputationNode_Out(secure_computation_nodes=response_secure_computation_nodes)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


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
    try:
        from app.api.data_federations import get_data_federation

        query = {
            "researcher_id": str(current_user.id),
            "id": str(secure_computation_node_id),
        }
        secure_computation_node = await data_service.find_one(DB_COLLECTION_SECURE_COMPUTATION_NODE, query)
        secure_computation_node = SecureComputationNode_Db(**secure_computation_node)

        # Get the basic information of the data federation
        data_federation = await get_data_federation(secure_computation_node.data_federation_provision_id, current_user)

        # Add the organization information to the data federation
        data_researcher_basic_info = [
            organization
            for organization in data_federation.research_organizations
            if organization.id == current_user.organization_id
        ][0]

        dataset_basic_info = [
            dataset for dataset in data_federation.datasets if dataset.id == secure_computation_node.dataset_id
        ][0]

        # Get the basic information of the data version
        dataset_version_basic_info = await get_dataset_version(secure_computation_node.dataset_version_id, current_user)

        response_secure_computation_node = GetSecureComputationNode_Out(
            **secure_computation_node.dict(),
            data_federation=BasicObjectInfo(_id=data_federation.id, name=data_federation.name),
            dataset=dataset_basic_info,
            dataset_version=BasicObjectInfo(_id=dataset_version_basic_info.id, name=dataset_version_basic_info.name),
            data_owner=dataset_version_basic_info.organization,
            researcher=data_researcher_basic_info,
            researcher_user=current_user.id,
        )

        return response_secure_computation_node
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


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
    try:
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

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
async def deprovision_secure_computation_nodes(
    background_tasks: BackgroundTasks,
    data_federation_provision_id: PyObjectId,
    current_user: TokenData = Depends(get_current_user),
):
    try:
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
        background_tasks.add_task(delete_resource_group, data_federation_provision_id, current_user)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
# TODO: these are temporary functions. They should be removed after the HANU is ready
def provision_virtual_machine(secure_computation_node_db: SecureComputationNode_Db):
    try:
        # Update the database to mark the VM as being created
        secure_computation_node_db.state = SecureComputationNodeState.CREATING
        sync_data_service.update_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE,
            {"_id": str(secure_computation_node_db.id)},
            {"$set": jsonable_encoder(secure_computation_node_db)},
        )

        # The name of the resource group is same as the data federation provision id
        owner = get_secret("owner")
        deployment_name = f"{owner}-{str(secure_computation_node_db.data_federation_provision_id)}-scn"

        # Deploy the secure computation node
        account_credentials = azure.authenticate(
            get_secret("azure_client_id"),
            get_secret("azure_client_secret"),
            get_secret("azure_tenant_id"),
            get_secret("azure_subscription_id"),
        )
        deploy_response: azure.DeploymentResponse = azure.deploy_module(
            account_credentials, deployment_name, "securecomputationnode", "Standard_D4s_v4"
        )
        if deploy_response.status != "Success":
            raise Exception(deploy_response.note)

        # Update the database to mark the VM as INITIALIZING
        secure_computation_node_db.ipaddress = IPv4Address(deploy_response.ip_address)
        secure_computation_node_db.state = SecureComputationNodeState.INITIALIZING
        sync_data_service.update_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE,
            {"_id": str(secure_computation_node_db.id)},
            {"$set": jsonable_encoder(secure_computation_node_db)},
        )

        # Create a SCN initialization vector json
        securecomputationnode_json = {}
        securecomputationnode_json[
            "NameOfVirtualMachine"
        ] = "{secure_computation_node_db.dataset_id}-{secure_computation_node_db.data_federation_provision_id}"
        securecomputationnode_json["IpAddressOfVirtualMachine"] = deploy_response.ip_address
        securecomputationnode_json["VirtualMachineIdentifier"] = str(secure_computation_node_db.id)
        securecomputationnode_json["ClusterIdentifier"] = str(uuid4())
        securecomputationnode_json["DigitalContractIdentifier"] = str(secure_computation_node_db.data_federation_id)
        securecomputationnode_json["RootOfTrustDomainIdentifier"] = str(uuid4())
        securecomputationnode_json["ComputationalDomainIdentifier"] = str(uuid4())
        securecomputationnode_json["DataConnectorDomainIdentifier"] = str(uuid4())
        securecomputationnode_json["DatasetIdentifier"] = str(secure_computation_node_db.dataset_id)
        securecomputationnode_json["VmEosb"] = "TODO"

        with open(deployment_name, "w") as outfile:
            json.dump(securecomputationnode_json, outfile)

        # Sleeping for 1.5 minutes
        time.sleep(90)

        headers = {"accept": "application/json"}
        files = {
            "initialization_vector": open(deployment_name, "rb"),
            "bin_package": open("SecureComputationNode.tar.gz", "rb"),
        }
        response = requests.put(
            "https://" + deploy_response.ip_address + ":9090/initialization-data",
            headers=headers,
            files=files,
            verify=False,
        )
        print("Upload package status: ", response.status_code)

        # Update the database to mark the VM as WAITING_FOR_DATA
        secure_computation_node_db.state = SecureComputationNodeState.WAITING_FOR_DATA
        sync_data_service.update_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE,
            {"_id": str(secure_computation_node_db.id)},
            {"$set": jsonable_encoder(secure_computation_node_db)},
        )

    except Exception as exception:
        print(exception)
        # Update the database to mark the VM as FAILED
        secure_computation_node_db.state = SecureComputationNodeState.FAILED
        secure_computation_node_db.detail = str(exception)
        sync_data_service.update_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE,
            {"_id": str(secure_computation_node_db.id)},
            {"$set": jsonable_encoder(secure_computation_node_db)},
        )


########################################################################################################################
def delete_resource_group(data_federation_provision_id: PyObjectId, current_user: TokenData):
    try:
        # Delete the scn resource group
        owner = get_secret("owner")
        deployment_name = f"{owner}-{str(data_federation_provision_id)}-scn"

        account_credentials = azure.authenticate(
            get_secret("azure_client_id"),
            get_secret("azure_client_secret"),
            get_secret("azure_tenant_id"),
            get_secret("azure_subscription_id"),
        )

        delete_response = azure.delete_resouce_group(account_credentials, deployment_name)
        if delete_response.status != "Success":
            raise Exception(delete_response.note)

        # Update the secure computation node
        sync_data_service.update_many(
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
        sync_data_service.update_many(
            DB_COLLECTION_SECURE_COMPUTATION_NODE,
            {
                "data_federation_provision_id": str(data_federation_provision_id),
                "researcher_id": str(current_user.organization_id),
            },
            {"$set": {"state": "DELETE_FAILED"}},
        )
