import React, { ReactElement } from 'react';

import { Route, Navigate } from 'react-router-dom';

import { IProtectedRoutes } from './ProtectedRoute.types';

import Spinner from '@components/Spinner';

const ProtectedRoute: React.FC<IProtectedRoutes> = ({
  userState,
  children,
  redirect,
  userData,
}): ReactElement => {
  // check if user finished loading, else run spinner
  if (userState !== 'isLoading' && userState !== null) {
    // if there is not user, render register page
    if (userData === null) {
      return <Navigate replace to={redirect} />;
    }
    // if there is a user, redirect to dashboard dashboard
    return children;
  }
  //@ts-ignore
  if (userState === 'noUserSession') {
    return <Navigate replace to={redirect} />;
  }
  return <Spinner />;
};

export default ProtectedRoute;
