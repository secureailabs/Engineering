import { IState } from '@app/redux/root-reducer';

export const selectFeed = (state: IState): IState['feed'] => state['feed'];
