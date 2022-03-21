import { IState } from '@redux/root-reducer';

export const selectAzureTemplatesManager = (
  state: IState
): IState['azureTemplatesManager'] => state['azureTemplatesManager'];
