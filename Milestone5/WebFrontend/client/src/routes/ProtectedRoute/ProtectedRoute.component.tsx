import React, { ReactElement } from 'react';

import { Route, Redirect } from 'react-router-dom';

import { IProtectedRoutes } from './ProtectedRoute.types';

import Spinner from '@components/Spinner';

const ProtectedRoute: React.FC<IProtectedRoutes> = ({
  exact,
  userState,
  children,
  redirect,
  userData,
  path,
}): ReactElement => (
  <>
    {exact ? (
      <Route
        // we don't want users to access the dashboard while not logged in
        exact
        path={path}
        render={(): ReactElement => {
          // check if user finished loading, else run spinner
          if (userState !== 'isLoading' && userState !== null) {
            // if there is not user, render register page
            if (userData === null) {
              return <Redirect to={redirect} />;
            }
            // if there is a user, redirect to dashboard dashboard
            return <>{children}</>;
          }
          if (userState == null && userData == null) {
            return <Redirect to={redirect} />;
          }
          return <Spinner />;
        }}
      />
    ) : (
      <Route
        // we don't want users to access the dashboard while not logged in
        path={path}
        render={(): ReactElement => {
          // check if user finished loading, else run spinner
          if (userState !== 'isLoading' && userState !== null) {
            // if there is not user, render register page
            if (userData === null) {
              return <Redirect to={redirect} />;
            }
            // if there is a user, redirect to dashboard dashboard
            return <>{children}</>;
          }
          //@ts-ignore
          if (userState === 'noUserSession') {
            return <Redirect to={redirect} />;
          }
          return <Spinner />;
        }}
      />
    )}
  </>
);

export default ProtectedRoute;
