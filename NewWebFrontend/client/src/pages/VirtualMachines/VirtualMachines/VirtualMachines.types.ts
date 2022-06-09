import { AxiosError } from 'axios';

import { TGetAllVirtualMachinesSuccess } from '@APIs/virtualMachineManager/virtualMachineManager.typedefs';
import { IConditionalRender } from '@components/ConditionalRenderRQuery/ConditionalRender/ConditionalRender.types';


export type TVirtualMachinesProps = {
    status: IConditionalRender['status'];
    getAllDatasetsData: TGetAllVirtualMachinesSuccess['secure_computation_nodes'];
    error: AxiosError<any>;
};

export type TVirtualMachinesFailureProps = {
    error: AxiosError<any>;
}

export type TVirtualMachinesSuccessProps = {
  getAllVirtualMachinesData: TGetAllVirtualMachinesSuccess;
};
