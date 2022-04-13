import { IState } from '@redux/root-reducer';

export const selectUnifiedRegistry = (
  state: IState
): IState['unifiedRegistry'] => state['unifiedRegistry'];
