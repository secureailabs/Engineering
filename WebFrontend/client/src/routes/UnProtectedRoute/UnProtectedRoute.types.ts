import { ReactElement } from 'react';

export interface IUnProtectedRoutes {
  children: ReactElement;
  exact: boolean;
  path: string;
  redirect: string;
  userState: any;
}

export interface IUnProtectedRoutesContainer {
  children: ReactElement;
  exact: boolean;
  path: string;
  redirect: string;
}