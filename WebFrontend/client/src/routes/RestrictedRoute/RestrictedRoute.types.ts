import { ReactElement } from 'react';

import { IState } from '@app/redux/root-reducer';

export interface IRestrictedRoutes {
  children: ReactElement;
  exact: boolean;
  path: string;
  requiredAccessRights: number;
  redirect: string;
  userData: IState['user']['userData'];
  userState: IState['user']['userState'];
}
