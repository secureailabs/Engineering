import { IState } from '@redux/root-reducer';

export const selectFeed = (state: IState): IState['feed'] => state['feed'];
