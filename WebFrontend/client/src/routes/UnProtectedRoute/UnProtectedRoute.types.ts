import { ReactElement } from 'react';

import { IState } from '@redux/root-reducer';

export interface IUnProtectedRoutes {
  children: ReactElement;
  exact: boolean;
  path: string;
  redirect: string;
}
