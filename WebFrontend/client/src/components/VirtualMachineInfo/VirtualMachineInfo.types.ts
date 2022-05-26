import { IDefaults } from '@APIs/typedefs';
import { TGetVirtualMachineSuccess } from '@app/redux/virtualMachineManager/virtualMachineManager.typeDefs';
import { IUserData } from '@APIs/user/user.typeDefs';

export type TVirtualMachineInfoSuccess = {
  getVirtualMachineData: TGetVirtualMachineSuccess | null;
  userData: IUserData;
  virtualMachineID: string;
};

export type TVirtualMachineInfo = {
  getVirtualMachineStart(key: string): void;
  getVirtualMachineReset(): void;
  getVirtualMachineState: IDefaults['state'];
  getVirtualMachineData: TGetVirtualMachineSuccess | null;
  virtualMachineID: string;
  userData: IUserData;
};
