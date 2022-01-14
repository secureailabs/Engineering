import * as React from 'react';
import { Redirect, Switch } from 'react-router-dom';

import Dashboard from '@pages/Dashboard';
import Login from '@pages/Login';
import Signup from '@pages/Signup';

import ProtectedRoute from './ProtectedRoute';
import UnProtectedRoute from './UnProtectedRoute';

const AppRouter: React.FC = (): React.ReactElement => (
  <Switch>
    <UnProtectedRoute exact path="/login" redirect="/dashboard">
      <Login />
    </UnProtectedRoute>

    <UnProtectedRoute exact path="/signup" redirect="/dashboard">
      <Signup />
    </UnProtectedRoute>

    <ProtectedRoute exact={false} path="/dashboard" redirect="/login">
      <Dashboard />
    </ProtectedRoute>

    {/* Handle default routes */}
    <ProtectedRoute exact={false} path="" redirect="/login">
      <Redirect to="/dashboard" />
    </ProtectedRoute>
  </Switch>
);

export default AppRouter;
