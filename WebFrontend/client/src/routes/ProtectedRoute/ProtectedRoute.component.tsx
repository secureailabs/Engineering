import React, { ReactElement } from 'react';

import { Route, Navigate ,  useLocation } from 'react-router-dom';

import { IProtectedRoutes } from './ProtectedRoute.types';

import Spinner from '@components/Spinner';

const ProtectedRoute: React.FC<IProtectedRoutes> = ({
  userState,
  children,
  redirect,
  userData,
}): ReactElement => {
  const { pathname } = useLocation();

  // check if user finished loading, else run spinner
  if (userState !== 'isLoading' && userState !== null) {
    // if there is not user, render register page
    if (userData === null) {
    window.localStorage.setItem("login-redirect", pathname);

      return <Navigate replace to={redirect} />;
    }
    window.localStorage.removeItem("login-redirect");
    // if there is a user, redirect to dashboard dashboard
    return children;
  }
  //@ts-ignore
  if (userState === 'noUserSession') {
    window.localStorage.setItem("login-redirect", pathname);
    return <Navigate replace to={redirect} />;
  }
  return <Spinner />;
};

export default ProtectedRoute;
