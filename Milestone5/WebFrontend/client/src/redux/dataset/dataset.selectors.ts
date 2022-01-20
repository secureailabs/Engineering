import { IState } from '@redux/root-reducer';

export const selectDataset = (state: IState): IState['dataset'] =>
  state['dataset'];
