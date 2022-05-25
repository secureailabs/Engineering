import { TGetVirtualMachineSuccess } from '@app/redux/virtualMachineManager/virtualMachineManager.typeDefs';
import { IUserData } from '@APIs/user/user.typeDefs';
import { IDefaults } from '@APIs/typedefs';

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
