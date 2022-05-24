import { IState } from '@app/redux/root-reducer';

export const selectOrganization = (state: IState): IState['organization'] =>
  state['organization'];
