import React from 'react';
import { useQueryClient } from 'react-query';

import { IUnProtectedRoutesContainer } from './UnProtectedRoute.types';
import UnProtectedRoute from './UnProtectedRoute.component';

const UnProtectedRouteContainer: React.FC<IUnProtectedRoutesContainer> = (props) => {
    const userState = useQueryClient().getQueryState('userData')
  return UnProtectedRoute({ ...props, userState: userState})
}

export default UnProtectedRouteContainer;
