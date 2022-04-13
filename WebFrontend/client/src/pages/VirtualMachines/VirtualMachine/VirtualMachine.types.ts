import { TGetVirtualMachineSuccess } from '@redux/virtualMachineManager/virtualMachineManager.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TVirtualMachineProps = {
  getVirtualMachineStart(): void;
  getVirtualMachineReset(): void;
  getVirtualMachineState: IDefaults['state'];
  getVirtualMachineData: TGetVirtualMachineSuccess;
  userData: IUserData;
};

export type TVirtualMachineSuccessProps = {
  getVirtualMachineData: TGetVirtualMachineSuccess;
};
