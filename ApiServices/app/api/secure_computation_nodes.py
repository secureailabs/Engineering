########################################################################################################################
# @author Prawal Gangwar
# @brief APIs to manage secure computation nodes
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
########################################################################################################################

import json
import subprocess
from ipaddress import IPv4Address
from typing import List, Optional
from uuid import uuid4

import app.azure.azure as azure
from app.api.authentication import get_current_user
from app.api.datasets import get_dataset
from app.api.digital_contracts import get_digital_contract
from app.data import operations as data_service
from app.data import sync_operations as sync_data_service
from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from models.accounts import UserRole
from models.authentication import TokenData
from models.common import PyObjectId
from models.datasets import Dataset_Db
from models.digital_contracts import DigitalContract_Db, DigitalContractState
from models.secure_computation_nodes import (
    GetMultipleSecureComputationNode_Out,
    GetSecureComputationNode_Out,
    RegisterSecureComputationNode_In,
    RegisterSecureComputationNode_Out,
    SecureComputationNode_Db,
    SecureComputationNodeState,
    UpdateSecureComputationNode_In,
)

########################################################################################################################
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
    backgropund_tasks: BackgroundTasks,
    secure_computation_node_req: RegisterSecureComputationNode_In = Body(...),
    current_user: TokenData = Depends(get_current_user),
):
    try:
        # Check if any running secure computation node is already registered with the name
        secure_computation_node_db = await data_service.find_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE,
            {"name": secure_computation_node_req.name, "researcher_id": str(current_user.organization_id)},
        )
        if secure_computation_node_db is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Secure Computation Node already registered"
            )

        # Check if the digital contract and dataset exist
        # TODO: Prawal make a HTTP request or use message queues
        dataset_db = await get_dataset(secure_computation_node_req.dataset_id, current_user)
        if dataset_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
        dataset_db = Dataset_Db(**dataset_db)

        # Check if the digital contract exists
        digital_contract_db = await get_digital_contract(secure_computation_node_req.digital_contract_id, current_user)
        if digital_contract_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Digital Contract not found")
        digital_contract_db = DigitalContract_Db(**digital_contract_db)

        # Digital Contract must be activated
        if digital_contract_db.state != DigitalContractState.ACTIVATED:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Digital Contract not activated")

        # Check if the digital contract and dataset match each other
        if dataset_db.id != digital_contract_db.dataset_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Dataset and Digital Contract do not match"
            )

        # Add the secure computation node to the database
        secure_computation_node_db = SecureComputationNode_Db(
            **secure_computation_node_req.dict(),
            researcher_user_id=current_user.organization_id,
            state=SecureComputationNodeState.REQUESTED,
            researcher_id=current_user.organization_id,
            data_owner_id=dataset_db.organization_id
        )
        await data_service.insert_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE, jsonable_encoder(secure_computation_node_db)
        )

        # Start the provisioning of the secure computation node in a background thread which will update the IP address
        backgropund_tasks.add_task(provision_virtual_machine, secure_computation_node_db)

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
        if (data_owner_id is not None) and (data_owner_id == current_user.organization_id):
            query = {"data_owner_id": str(data_owner_id)}
        elif (researcher_id is not None) and (researcher_id == current_user.organization_id):
            query = {"researcher_id": str(researcher_id)}
        elif current_user.role is UserRole.SAIL_ADMIN:
            query = {}
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        secure_computation_nodes = await data_service.find_by_query(DB_COLLECTION_SECURE_COMPUTATION_NODE, query)
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
        if secure_computation_node is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secure Computation Node not found")

        secure_computation_node_db = SecureComputationNode_Db(**secure_computation_node)
        if (
            (secure_computation_node_db.data_owner_id != current_user.organization_id)
            and (secure_computation_node_db.researcher_id != current_user.organization_id)
            and (current_user.role != UserRole.SAIL_ADMIN)
        ):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

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
        if secure_computation_node_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secure Computation Node not found")
        secure_computation_node_db = SecureComputationNode_Db(**secure_computation_node_db)

        # Only researcher credentials can mark a secure computation node as running
        if secure_computation_node_db.state == SecureComputationNodeState.INITIALIZING:
            if updated_secure_computation_node_info.state == SecureComputationNodeState.READY:
                secure_computation_node_db.state = SecureComputationNodeState.READY
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
    backgropund_tasks: BackgroundTasks,
    secure_computation_node_id: PyObjectId,
    current_user: TokenData = Depends(get_current_user),
):
    try:
        # Check if the secure computation node exists
        secure_computation_node_db = await data_service.find_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE, {"_id": str(secure_computation_node_id)}
        )
        if secure_computation_node_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secure Computation Node not found")
        secure_computation_node_db = SecureComputationNode_Db(**secure_computation_node_db)

        # Only researcher can disable a secure computation node
        if secure_computation_node_db.researcher_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        secure_computation_node_db.state = SecureComputationNodeState.DELETING

        # TODO: Prawal do it later depending on HANU status
        # Start a background task to deprovision the secure computation node which will update the status
        backgropund_tasks.add_task(deprovision_virtual_machine, secure_computation_node_db)

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

        AZURE_SUBSCRIPTION_ID = "3d2b9951-a0c8-4dc3-8114-2776b047b15c"
        AZURE_TENANT_ID = "3e74e5ef-7e6a-4cf0-8573-680ca49b64d8"
        AZURE_CLIENT_ID = "4f909fab-ad4c-4685-b7a9-7ddaae4efb22"
        AZURE_CLIENT_SECRET = "1YEn1Y.bVTVk-dzm9voTWyf7DrgQF29xL2"
        OWNER = "fastapi"

        deployment_name = OWNER + str(secure_computation_node_db.id) + "-scn"

        # Deploy the secure computation node
        account_credentials = azure.authenticate(
            AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID, AZURE_SUBSCRIPTION_ID
        )
        deploy_response: azure.DeploymentResponse = azure.deploy_module(
            account_credentials, deployment_name, "securecomputationnode"
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

        upload_status = subprocess.run(
            [
                "./UploadPackageAndInitializationVector",
                "--IpAddress=" + deploy_response.ip_address,
                "--Package=SecureComputationNode.tar.gz",
                "--InitializationVector=" + deployment_name,
            ],
            stdout=subprocess.PIPE,
        )
        print("Upload status: ", upload_status.stdout)

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
        secure_computation_node_db.details = str(exception)
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

        AZURE_SUBSCRIPTION_ID = "3d2b9951-a0c8-4dc3-8114-2776b047b15c"
        AZURE_TENANT_ID = "3e74e5ef-7e6a-4cf0-8573-680ca49b64d8"
        AZURE_CLIENT_ID = "4f909fab-ad4c-4685-b7a9-7ddaae4efb22"
        AZURE_CLIENT_SECRET = "1YEn1Y.bVTVk-dzm9voTWyf7DrgQF29xL2"
        OWNER = "fastapi"

        # Delete the virtual machine resource group
        deployment_name = OWNER + str(secure_computation_node_db.id) + "-scn"

        account_credentials = azure.authenticate(
            AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID, AZURE_SUBSCRIPTION_ID
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
        secure_computation_node_db.details = str(exception)
        sync_data_service.update_one(
            DB_COLLECTION_SECURE_COMPUTATION_NODE,
            {"_id": str(secure_computation_node_db.id)},
            {"$set": jsonable_encoder(secure_computation_node_db)},
        )
