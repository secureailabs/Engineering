import { TGetVirtualMachineSuccess } from '@app/redux/virtualMachineManager/virtualMachineManager.typeDefs';
import { IUserData } from '@app/redux/user/user.typeDefs';
import { IDefaults } from '@app/redux/typedefs';

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
