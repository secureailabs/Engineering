import { ReactElement } from 'react';

export interface IRestrictedRoutes {
  children: ReactElement;
  exact: boolean;
  path: string;
  requiredAccessRights: string;
  redirect: string;
  userState: any;
}

export interface IRestrictedRoutesContainer {
  children: ReactElement;
  exact: boolean;
  path: string;
  requiredAccessRights: string;
  redirect: string;
}
