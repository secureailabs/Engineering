export type TGetAllVirtualMachinesSuccess = {
    secure_computation_nodes: Array<TGetVirtualMachineSuccess>;
}

export type TGetAllVirtualMachinesStart = {
    data_owner_id?: string;
    researcher_id?: string;
}

export type TGetVirtualMachineSuccess = {
    id: string;
    name: string;
    digital_contract: {
        id: string;
        name: string;
    }
    dataset: {
        id: string;
        name: string;
    }
    researcher: {
        id: string;
        name: string;
    }
    data_owner: {
        id: string;
        name: string;
    }
    researcher_user: {
        id: string;
        name: string;
    }
    type: string;
    timestamp: string;
    state: 'REQUESTED' | 'CREATING' | 'INITIALIZING' |
    'WAITING_FOR_DATA' | 'FAILED' | 'READY' |
    'IN_USE' | 'DELETED' | 'DELETING' | 'DELETE_FAILED';
    detail: string;
    ipaddress: string;
    
    // Types added for demo purposes only
    region?: string;
    launched_by?: {
        user_name: string;
        user_email: string;
        org_name: string;
        org_id: string;
    }
    uptime?: string;
}

export type TGetVirtualMachineStart = {
    secure_computation_node_id: string;
}