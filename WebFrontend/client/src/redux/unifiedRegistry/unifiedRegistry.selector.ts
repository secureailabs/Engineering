import { IState } from '@app/redux/root-reducer';

export const selectUnifiedRegistry = (
  state: IState
): IState['unifiedRegistry'] => state['unifiedRegistry'];
