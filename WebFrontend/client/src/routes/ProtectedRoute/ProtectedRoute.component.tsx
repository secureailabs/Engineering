import React, { ReactElement } from 'react';
import { useQueryClient } from 'react-query';
import { Route, Navigate ,  useLocation } from 'react-router-dom';

import { IProtectedRoutes } from './ProtectedRoute.types';

import Spinner from '@components/Spinner';

const ProtectedRoute: React.FC<IProtectedRoutes> = ({
  // userState,
  children,
  redirect,
}): ReactElement => {
  const userState = useQueryClient().getQueryState('userData')
  
  const { pathname } = useLocation();
  console.log(userState)
  // check if user finished loading, else run spinner
  if (userState && !userState.isFetching) {
    // if there is not user, render register page
    if (!userState.data || userState.error) {
    window.localStorage.setItem("login-redirect", pathname);

      return <Navigate replace to={redirect} />;
    }
    window.localStorage.removeItem("login-redirect");
    // if there is a user, redirect to dashboard dashboard
    return children;
  }

  return <Spinner />;
};

export default ProtectedRoute;
