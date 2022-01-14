import { IState } from '@redux/root-reducer';

export const selectAccountManager = (
  state: IState
): IState['accountManager'] => state['accountManager'];
