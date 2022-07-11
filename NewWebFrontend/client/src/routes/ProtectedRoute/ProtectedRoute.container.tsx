import React from 'react';

import { useQueryClient } from 'react-query';
import { IProtectedRoutesContainer } from './ProtectedRoute.types';
import ProtectedRoute from './ProtectedRoute.component';

const ProtectedRouteContainer: React.FC<IProtectedRoutesContainer> = (props) => {
  const userState = useQueryClient().getQueryState('userData')

  return ProtectedRoute({ ...props, userState: userState})
}

export default ProtectedRouteContainer;