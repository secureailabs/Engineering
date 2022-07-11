import React from 'react';
import { useQueryClient } from 'react-query';

import { IRestrictedRoutesContainer } from './RestrictedRoute.types';

import RestrictedRoute from './RestrictedRoute.component';


const RestrictedRouteContainer: React.FC<IRestrictedRoutesContainer> = (props) => {
  const userState = useQueryClient().getQueryState('userData')

  return RestrictedRoute({ ...props, userState: userState})
}

export default RestrictedRouteContainer;