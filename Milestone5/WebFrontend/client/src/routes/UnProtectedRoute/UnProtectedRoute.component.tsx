import React from 'react';

import { Route, Navigate } from 'react-router-dom';

import Spinner from '@components/Spinner';

import { IUnProtectedRoutes } from './UnProtectedRoute.types';

const UnprotectedRoute: React.FC<IUnProtectedRoutes> = ({
  exact,
  userState,
  children,
  redirect,
  userData,
  path,
}) => {
  return (
    <>
      {exact ? (
        <Route
          // we don't want users to access the dashboard while not logged in
          exact
          path={path}
          render={() => {
            // check if user finished loading, else run spinner
            if (
              userState === 'noUserSession' ||
              userState === 'failure' ||
              userState === 'signup-success'
            ) {
              // if there is not user, render register page
              if (userData === null) {
                return <>{children}</>;
              }
              // if there is a user, redirect to dashboard dashboard
              return <Navigate replace to={redirect} />;
            }
            if (userState === 'success' && userData !== null) {
              return <Navigate replace to={redirect} />;
            }
            return <Spinner />;
          }}
        />
      ) : (
        <Route
          // we don't want users to access the dashboard while not logged in
          path={path}
          render={() => {
            // check if user finished loading, else run spinner
            if (
              userState === 'noUserSession' ||
              userState === 'failure' ||
              userState === 'signup-success'
            ) {
              // if there is not user, render register page
              if (userData === null) {
                return <>{children}</>;
              }
              // if there is a user, redirect to dashboard dashboard
              return <Navigate replace to="/dashboard" />;
            }
            if (userState === 'success' && userData !== null) {
              return <Navigate replace to={redirect} />;
            }
            return <Spinner />;
          }}
        />
      )}
    </>
  );
};

export default UnprotectedRoute;
