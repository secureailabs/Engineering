import { IState } from '@app/redux/root-reducer';

export const selectAzureTemplate = (state: IState): IState['azureTemplate'] =>
  state['azureTemplate'];
