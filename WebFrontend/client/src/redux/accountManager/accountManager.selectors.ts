import { IState } from '@app/redux/root-reducer';

export const selectAccountManager = (
  state: IState
): IState['accountManager'] => state['accountManager'];
