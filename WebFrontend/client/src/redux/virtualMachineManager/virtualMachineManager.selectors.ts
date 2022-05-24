import { IState } from '@app/redux/root-reducer';

export const selectVirtualMachine = (
  state: IState
): IState['virtualMachineManager'] => state['virtualMachineManager'];
