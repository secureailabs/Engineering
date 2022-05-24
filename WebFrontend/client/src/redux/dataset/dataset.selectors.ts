import { IState } from '@app/redux/root-reducer';

export const selectDataset = (state: IState): IState['dataset'] =>
  state['dataset'];
