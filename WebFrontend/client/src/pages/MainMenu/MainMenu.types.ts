import { IState } from '@app/redux/root-reducer';

export interface IMainMenu {
  userData: IState['user']['userData'];
}
