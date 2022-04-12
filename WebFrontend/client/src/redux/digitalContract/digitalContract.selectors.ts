import { IState } from '@redux/root-reducer';

export const selectDigitalContract = (
  state: IState
): IState['digitalContract'] => state['digitalContract'];
