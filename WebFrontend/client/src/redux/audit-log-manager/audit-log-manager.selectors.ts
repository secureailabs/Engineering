import { IState } from '@redux/root-reducer';

export const selectContact = (state: IState): IState['audit-log-manager'] =>
  state['audit-log-manager'];
