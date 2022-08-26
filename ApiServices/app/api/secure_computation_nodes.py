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
from typing import Optional
from uuid import uuid4

import app.utils.azure as azure
import requests
from app.api.accounts import get_user
from app.api.authentication import get_current_user
from app.api.dataset_versions import get_dataset_version
from app.api.digital_contracts import get_digital_contract
from app.data import operations as data_service
from app.data import sync_operations as sync_data_service
from app.utils.secrets import get_secret
from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from models.accounts import UserRole
from models.authentication import TokenData
from models.common import PyObjectId
from models.dataset_versions import GetDatasetVersion_Out
from models.digital_contracts import DigitalContractState
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
@router.post(
    path="/secure-computation-node",
    description="Register new secure computation node",
    response_description="Secure Computation Node Id",
    response_model=RegisterSecureComputationNode_Out,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
)
async def register_secure_computation_node(
    background_tasks: BackgroundTasks,
    secure_computation_node_req: RegisterSecureComputationNode_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
):
    try:
        # Check if any running secure computation node is already registered with the name
        secure_computation_node_db = await data_service.find_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE,
            {"name": secure_computation_node_req.name, "researcher_id": str(current_user.organization_id)},
        )
        if secure_computation_node_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Secure Computation Node already registered"
            )

        # Check if the digital contract and dataset exist
        # TODO: Prawal make a HTTP request or use message queues
        dataset_db = await get_dataset_version(secure_computation_node_req.dataset_id, current_user)
        if not dataset_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

        # Check if the digital contract exists
        digital_contract_db = await get_digital_contract(secure_computation_node_req.digital_contract_id, current_user)
        if not digital_contract_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Digital Contract not found")

        # Digital Contract must be activated
        if digital_contract_db.state != DigitalContractState.ACTIVATED:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Digital Contract not activated")

        # Check if the digital contract and dataset match each other
        if dataset_db.id != digital_contract_db.dataset.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Dataset and Digital Contract do not match"
            )

        # Add the secure computation node to the database
        secure_computation_node_db = SecureComputationNode_Db(
            **secure_computation_node_req.dict(),
            researcher_user_id=current_user.id,
            state=SecureComputationNodeState.REQUESTED,
            researcher_id=current_user.organization_id,
            data_owner_id=dataset_db.organization.id,
        )
        await data_service.insert_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE, jsonable_encoder(secure_computation_node_db)
        )

        # Start the provisioning of the secure computation node in a background thread which will update the IP address
        background_tasks.add_task(provision_virtual_machine, secure_computation_node_db)

        return secure_computation_node_db
    except HTTPException as http_exception:
        raise http_exception
    except Exception as exception:
        raise exception


########################################################################################################################
@router.get(
    path="/secure-computation-node",
    description="Get list of all the secure_computation_node",
    response_description="List of secure_computation_node",
    response_model=GetMultipleSecureComputationNode_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_all_secure_computation_nodes(
    data_owner_id: Optional[PyObjectId] = None,
    researcher_id: Optional[PyObjectId] = None,
    current_user: TokenData = Depends(get_current_user),
):
    try:
        # TODO: Prawal the current user organization is repeated in the request, find a better way
        if (data_owner_id) and (data_owner_id == current_user.organization_id):
            query = {"data_owner_id": str(data_owner_id)}
        elif (researcher_id) and (researcher_id == current_user.organization_id):
            query = {"researcher_id": str(researcher_id)}
        elif current_user.role is UserRole.SAIL_ADMIN:
            query = {}
        elif (not researcher_id) and (not data_owner_id):
            query = {
                "$or": [
                    {"researcher_id": str(current_user.organization_id)},
                    {"data_owner_id": str(current_user.organization_id)},
                ]
            }
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        secure_computation_nodes = await data_service.find_by_query(DB_COLLECTION_SECURE_COMPUTATION_NODE, query)

        # Cache the organization information
        digital_contract_cache = {}
        user_cache = {}

        for secure_computation_node in secure_computation_nodes:
            # Add the data owner, researcher and dataset information to the secure computation node from digital contract
            if secure_computation_node["digital_contract_id"] not in digital_contract_cache:
                digital_contract_cache[secure_computation_node["digital_contract_id"]] = await get_digital_contract(
                    digital_contract_id=secure_computation_node["digital_contract_id"], current_user=current_user
                )
            secure_computation_node["digital_contract"] = digital_contract_cache[
                secure_computation_node["digital_contract_id"]
            ]
            secure_computation_node["researcher"] = digital_contract_cache[
                secure_computation_node["digital_contract_id"]
            ].researcher
            secure_computation_node.pop("researcher_id")
            secure_computation_node["data_owner"] = digital_contract_cache[
                secure_computation_node["digital_contract_id"]
            ].data_owner
            secure_computation_node.pop("data_owner_id")
            secure_computation_node["dataset"] = digital_contract_cache[
                secure_computation_node["digital_contract_id"]
            ].dataset

            secure_computation_node.pop("digital_contract_id")
            secure_computation_node.pop("dataset_id")

            # Add the user information to the secure computation node
            if secure_computation_node["researcher_user_id"] not in user_cache:
                user_cache[secure_computation_node["researcher_user_id"]] = await get_user(
                    organization_id=secure_computation_node["researcher"].id,
                    user_id=secure_computation_node["researcher_user_id"],
                    current_user=current_user,
                )
            secure_computation_node["researcher_user"] = user_cache[secure_computation_node["researcher_user_id"]]
            secure_computation_node.pop("researcher_user_id")

        return GetMultipleSecureComputationNode_Out(secure_computation_nodes=secure_computation_nodes)
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
        secure_computation_node = await data_service.find_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE, {"_id": str(secure_computation_node_id)}
        )
        if not secure_computation_node:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secure Computation Node not found")

        secure_computation_node_db = SecureComputationNode_Db(**secure_computation_node)
        if (
            (secure_computation_node_db.data_owner_id != current_user.organization_id)
            and (secure_computation_node_db.researcher_id != current_user.organization_id)
            and (current_user.role != UserRole.SAIL_ADMIN)
        ):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        # Add the data owner, researcher and dataset information to the secure computation node from digital contract
        digital_contract = await get_digital_contract(
            digital_contract_id=secure_computation_node["digital_contract_id"], current_user=current_user
        )
        secure_computation_node["digital_contract"] = digital_contract
        secure_computation_node["researcher"] = digital_contract.researcher
        secure_computation_node["data_owner"] = digital_contract.data_owner
        secure_computation_node["dataset"] = digital_contract.dataset
        secure_computation_node.pop("dataset_id")
        secure_computation_node.pop("researcher_id")
        secure_computation_node.pop("data_owner_id")
        secure_computation_node.pop("digital_contract_id")

        # Add the user information to the secure computation node
        secure_computation_node["researcher_user"] = await get_user(
            organization_id=digital_contract.researcher.id,
            user_id=secure_computation_node["researcher_user_id"],
            current_user=current_user,
        )
        secure_computation_node.pop("researcher_user_id")

        return secure_computation_node
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
        secure_computation_node_db = SecureComputationNode_Db(**secure_computation_node_db)

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
@router.delete(
    path="/secure-computation-node/{secure_computation_node_id}",
    description="Deprovision the secure_computation_node",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def deprovision_secure_computation_node(
    background_tasks: BackgroundTasks,
    secure_computation_node_id: PyObjectId,
    current_user: TokenData = Depends(get_current_user),
):
    try:
        # Check if the secure computation node exists
        secure_computation_node_db = await data_service.find_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE, {"_id": str(secure_computation_node_id)}
        )
        if not secure_computation_node_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secure Computation Node not found")
        secure_computation_node_db = SecureComputationNode_Db(**secure_computation_node_db)

        # Only researcher can disable a secure computation node
        if secure_computation_node_db.researcher_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        secure_computation_node_db.state = SecureComputationNodeState.DELETING

        # TODO: Prawal do it later depending on HANU status
        # Start a background task to deprovision the secure computation node which will update the status
        background_tasks.add_task(deprovision_virtual_machine, secure_computation_node_db)

        # Update the secure computation node
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
# TODO: Prawal these are temporary functions. They should be removed after the HANU is ready
def provision_virtual_machine(secure_computation_node_db: SecureComputationNode_Db):
    try:
        # Update the database to mark the VM as being created
        secure_computation_node_db.state = SecureComputationNodeState.CREATING
        sync_data_service.update_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE,
            {"_id": str(secure_computation_node_db.id)},
            {"$set": jsonable_encoder(secure_computation_node_db)},
        )
        owner = get_secret("owner")
        deployment_name = f"{owner}-{str(secure_computation_node_db.id)}-scn"

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
        securecomputationnode_json["NameOfVirtualMachine"] = secure_computation_node_db.name
        securecomputationnode_json["IpAddressOfVirtualMachine"] = deploy_response.ip_address
        securecomputationnode_json["VirtualMachineIdentifier"] = str(secure_computation_node_db.id)
        securecomputationnode_json["ClusterIdentifier"] = str(uuid4())
        securecomputationnode_json["DigitalContractIdentifier"] = str(secure_computation_node_db.digital_contract_id)
        securecomputationnode_json["RootOfTrustDomainIdentifier"] = str(uuid4())
        securecomputationnode_json["ComputationalDomainIdentifier"] = str(uuid4())
        securecomputationnode_json["DataConnectorDomainIdentifier"] = str(uuid4())
        securecomputationnode_json["DatasetIdentifier"] = str(secure_computation_node_db.dataset_id)
        securecomputationnode_json["VmEosb"] = "TODO"

        with open(deployment_name, "w") as outfile:
            json.dump(securecomputationnode_json, outfile)

        # Sleeping for two minutes
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
def deprovision_virtual_machine(secure_computation_node_db: SecureComputationNode_Db):
    try:
        secure_computation_node_db.ipaddress = IPv4Address("0.0.0.0")
        secure_computation_node_db.state = SecureComputationNodeState.DELETING
        sync_data_service.update_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE,
            {"_id": str(secure_computation_node_db.id)},
            {"$set": jsonable_encoder(secure_computation_node_db)},
        )

        # Delete the virtual machine resource group
        owner = get_secret("owner")
        deployment_name = f"{owner}-{str(secure_computation_node_db.id)}-scn"

        account_credentials = azure.authenticate(
            get_secret("azure_client_id"),
            get_secret("azure_client_secret"),
            get_secret("azure_tenant_id"),
            get_secret("azure_subscription_id"),
        )

        delete_response = azure.delete_resouce_group(account_credentials, deployment_name)
        if delete_response.status != "Success":
            raise Exception(delete_response.note)

        secure_computation_node_db.ipaddress = IPv4Address("0.0.0.0")
        secure_computation_node_db.state = SecureComputationNodeState.DELETED
        sync_data_service.update_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE,
            {"_id": str(secure_computation_node_db.id)},
            {"$set": jsonable_encoder(secure_computation_node_db)},
        )
    except Exception as exception:
        print(exception)
        # Update the database to mark the VM as FAILED
        secure_computation_node_db.state = SecureComputationNodeState.DELETE_FAILED
        secure_computation_node_db.detail = str(exception)
        sync_data_service.update_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE,
            {"_id": str(secure_computation_node_db.id)},
            {"$set": jsonable_encoder(secure_computation_node_db)},
        )
