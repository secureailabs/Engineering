import { IState } from '@app/redux/root-reducer';

export const selectDigitalContract = (
  state: IState
): IState['digitalContract'] => state['digitalContract'];
