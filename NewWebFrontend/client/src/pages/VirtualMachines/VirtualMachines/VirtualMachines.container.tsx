import { useQuery } from 'react-query';
import { AxiosError } from 'axios';

import { TGetAllVirtualMachinesSuccess } from '@APIs/virtualMachineManager/virtualMachineManager.typedefs';

import { getAllVirtualMachinesAPIdemo } from '@APIs/virtualMachineManager/virtualMachineManager.demo-apis';

import Datasets from './VirtualMachines.component';

const VirtualMachinesContainer: React.FC = () => {
    // const apiFunction = localStorage.getItem('mode') == 'demo' ? getAllDatasetsAPIdemo : getAllDatasetsAPI;
    const apiFunction = getAllVirtualMachinesAPIdemo;


    const { data, isLoading, status, error, refetch } =
        // @ts-ignore
        useQuery<TGetAllDatasetsSuccess['datasets'], AxiosError>(['datasets'], apiFunction, { refetchOnMount: 'always' });
    //@ts-ignore
    return Datasets({ status: status, getAllDatasetsData: data, error: error })

}

export default VirtualMachinesContainer;
