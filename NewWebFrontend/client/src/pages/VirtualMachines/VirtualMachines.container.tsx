import { useQuery, useQueryClient } from 'react-query';
import { AxiosError } from 'axios';

import { TGetAllVirtualMachinesSuccess } from '@APIs/virtualMachineManager/virtualMachineManager.typedefs';

import { getAllVirtualMachinesAPIdemo } from '@APIs/virtualMachineManager/virtualMachineManager.demo-apis';

import VirtualMachines from './VirtualMachines.component';

const VirtualMachinesContainer: React.FC = () => {
    const userData = useQueryClient().getQueryData('userData')
    
    const apiFunction = getAllVirtualMachinesAPIdemo;

    const { data, status, error } =
        // @ts-ignore
        useQuery<TGetAllVirtualMachinesSuccess['secure_computation_nodes'], AxiosError>(['datasets'], apiFunction, { refetchOnMount: 'always' });
    //@ts-ignore
    return VirtualMachines({ status: status, getAllVirtualMachinesData: data, error: error, userData: userData })

}

export default VirtualMachinesContainer;
