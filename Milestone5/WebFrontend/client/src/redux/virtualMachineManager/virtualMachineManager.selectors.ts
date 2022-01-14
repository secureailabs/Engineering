import { IState } from '@redux/root-reducer';

export const selectVirtualMachine = (
  state: IState
): IState['virtualMachineManager'] => state['virtualMachineManager'];
