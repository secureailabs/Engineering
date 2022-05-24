import { TGetAllVirtualMachinesSuccess } from '@app/redux/virtualMachineManager/virtualMachineManager.typeDefs';
import { IUserData } from '@app/redux/user/user.typeDefs';
export type TVirtualMachineList = {
  setVirtualMachineID(digitalContract: string): void;
  data: Array<
    TGetAllVirtualMachinesSuccess['VirtualMachines']['VirtualMachinesAssociatedWithDc']['']
  >;
};
