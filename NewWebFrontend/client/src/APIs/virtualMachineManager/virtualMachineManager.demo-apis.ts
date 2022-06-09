import { AxiosError, AxiosResponse } from 'axios';

import {
    TGetVirtualMachineStart,
    TGetAllVirtualMachinesStart,
    TGetVirtualMachineSuccess,
    TGetAllVirtualMachinesSuccess,
} from './virtualMachineManager.typedefs';

import demo_data from './virtualMachine.data';

export const getVirtualMachineAPIdemo = async (data: TGetVirtualMachineStart): Promise<TGetVirtualMachineSuccess> => {
    const index = parseInt(data.secure_computation_node_id.slice(-1)) - 1
    return demo_data.secure_computation_nodes[index]
}

export const getAllVirtualMachinesAPIdemo = async (data: TGetAllVirtualMachinesStart): Promise<TGetAllVirtualMachinesSuccess> => {
    return demo_data
}
