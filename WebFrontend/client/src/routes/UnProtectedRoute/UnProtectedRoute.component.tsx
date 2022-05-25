import React, { ReactElement } from 'react';

import { useQueryClient } from 'react-query';

import { Navigate } from 'react-router-dom';

import { IUnProtectedRoutes } from './UnProtectedRoute.types';

import { AbsoluteSpinner } from '@components/Spinner';

const UnProtectedRoute: React.FC<IUnProtectedRoutes> = ({
  children,
  redirect,
}): ReactElement => {
  const userState = useQueryClient().getQueryState('userData')

  // check if user finished loading, else run spinner
  if (!userState?.isFetching) {
    // if there is not user, render register page
    if (userState?.data !== undefined && !userState.error) {
      return <Navigate replace to={window.localStorage.getItem("login-redirect") || redirect} />;
    }
    // if there is a user, redirect to dashboard dashboard
    return children;
  }

  return <AbsoluteSpinner />;
  // return children;
};

export default UnProtectedRoute;
