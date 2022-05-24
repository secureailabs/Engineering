import { TGetAllVirtualMachinesSuccess } from '@app/redux/virtualMachineManager/virtualMachineManager.typeDefs';
import { IUserData } from '@app/redux/user/user.typeDefs';
import { IDefaults } from '@app/redux/typedefs';

export type TVirtualMachinesProps = {
  getAllVirtualMachinesStart(): void;
  getAllVirtualMachinesReset(): void;
  getAllVirtualMachinesState: IDefaults['state'];
  getAllVirtualMachinesData: TGetAllVirtualMachinesSuccess;
  userData: IUserData;
};

export type TVirtualMachinesSuccessProps = {
  getAllVirtualMachinesData: TGetAllVirtualMachinesSuccess;
};
