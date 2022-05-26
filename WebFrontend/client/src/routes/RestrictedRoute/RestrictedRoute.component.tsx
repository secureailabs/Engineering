// @ts-nocheck
import React, { ReactElement } from 'react';

import { Route, Navigate } from 'react-router-dom';

import { IRestrictedRoutes } from './RestrictedRoute.types';

import Spinner from '@components/Spinner';

const RestrictedRoute: React.FC<IRestrictedRoutes> = ({
  exact,
  userState,
  children,
  redirect,
  path,
  requiredAccessRights,
}): ReactElement => (
  <>
    {exact ? (
      <Route
        // we don't want users to access the dashboard while not logged in
        exact
        path={path}
        render={(): ReactElement => {
          // check if user finished loading, else run spinner
          if (!userState.isLoading && userState !== undefined) {
            // if there is not user, render register page
            if (
              userState.data === undefined ||
              userData.data.role != requiredAccessRights
            ) {
              return <Navigate replace to={redirect} />;
            }
            // if there is a user, redirect to dashboard dashboard
            return <>{children}</>;
          }
          if (userState == null && userState.data == null) {
            return <Navigate replace to={redirect} />;
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
          if (!userState.isLoading && userState !== null) {
            // if there is not user, render register page
            if (
              userState.data === null ||
              userState.data.role != requiredAccessRights
            ) {
              return <Navigate replace to={redirect} />;
            }
            // if there is a user, redirect to dashboard dashboard
            return <>{children}</>;
          }
          //@ts-ignore
          if (userState === 'noUserSession') {
            return <Navigate replace to={redirect} />;
          }
          return <Spinner />;
        }}
      />
    )}
  </>
);

export default RestrictedRoute;
