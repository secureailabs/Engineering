import { ReactElement } from 'react';
import { QueryClient } from 'react-query';
import { IState } from '@app/redux/root-reducer';

export interface IProtectedRoutes {
  children: ReactElement;
  redirect: string;
  userState: QueryClient['getQueryState'];
}
