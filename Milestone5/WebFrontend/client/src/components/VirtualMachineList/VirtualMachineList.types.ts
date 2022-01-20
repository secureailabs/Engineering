import { TGetAllVirtualMachinesSuccess } from '@redux/virtualMachineManager/virtualMachineManager.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';
export type TVirtualMachineList = {
  setVirtualMachineID(digitalContract: string): void;
  data: Array<
    TGetAllVirtualMachinesSuccess['VirtualMachines']['VirtualMachinesAssociatedWithDc']['']
  >;
};
