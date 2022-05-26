import { ReactElement } from 'react';

export interface IProtectedRoutes {
  children: ReactElement;
  redirect: string;
  userState: any;
}

export interface IProtectedRoutesContainer {
  children: ReactElement;
  redirect: string;
}