import { AxiosError } from 'axios';

import { TGetAllVirtualMachinesSuccess } from '@APIs/virtualMachineManager/virtualMachineManager.typedefs';
import { IConditionalRender } from '@components/ConditionalRenderRQuery/ConditionalRender/ConditionalRender.types';
import { IUserData } from '@APIs/user/user.typeDefs';


export type TVirtualMachinesProps = {
  status: IConditionalRender['status'];
  userData: IUserData;
  getAllVirtualMachinesData: TGetAllVirtualMachinesSuccess;
  error: AxiosError<any>;
};

export type TVirtualMachinesFailureProps = {
  error: AxiosError<any>;
}

export type TVirtualMachinesSuccessProps = {
  userData: IUserData;
  getAllVirtualMachinesData: TGetAllVirtualMachinesSuccess;
};
