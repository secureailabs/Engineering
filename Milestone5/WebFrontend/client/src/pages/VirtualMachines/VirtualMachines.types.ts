import { TGetAllVirtualMachinesSuccess } from '@redux/virtualMachineManager/virtualMachineManager.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TVirtualMachinesProps = {
  getAllVirtualMachinesStart(): void;
  getAllVirtualMachinesReset(): void;
  getAllVirtualMachinesState: IDefaults['state'];
  getAllVirtualMachinesData: TGetAllVirtualMachinesSuccess;
  userData: IUserData;
};

export type TVirtualMachinesSuccessProps = {
  getAllVirtualMachinesData: TGetAllVirtualMachinesSuccess;
  userData: IUserData;
  stageView: TGetAllVirtualMachinesSuccess['']['ResearcherOrganization'];
  setVirtualMachineID(stage: TVirtualMachinesSuccessProps['stageView']): void;
};
