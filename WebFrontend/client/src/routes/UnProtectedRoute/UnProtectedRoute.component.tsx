import React, { ReactElement } from 'react';

import { Navigate } from 'react-router-dom';

import { IUnProtectedRoutes } from './UnProtectedRoute.types';

import Spinner from '@components/Spinner';

const ProtectedRoute: React.FC<IUnProtectedRoutes> = ({
  userState,
  children,
  redirect,
  userData,
}): ReactElement => {
  // check if user finished loading, else run spinner
  if (userState !== 'isLoading' && userState !== null) {
    // if there is not user, render register page
    if (userData !== null) {
      return <Navigate replace to={window.localStorage.getItem("login-redirect") || redirect} />;
    }
    // if there is a user, redirect to dashboard dashboard
    return children;
  }

  return <Spinner />;
};

export default ProtectedRoute;
