import * as React from 'react';
import { Navigate, Routes, Route } from 'react-router-dom';

import Dashboard from '@pages/Dashboard';
import Login from '@pages/Login';
import Signup from '@pages/Signup';

import ProtectedRoute from './ProtectedRoute';
import UnProtectedRoute from './UnProtectedRoute';
{
  /*
      *
      *
    <UnProtectedRoute exact path="/login" redirect="/dashboard">
      <Login />
    </UnProtectedRoute>

    <UnProtectedRoute exact path="/signup" redirect="/dashboard">
      <Signup />
    </UnProtectedRoute>
      *
   * <ProtectedRoute exact={false} path="/dashboard" redirect="/login">
      <Dashboard />
    </ProtectedRoute>
        <ProtectedRoute exact={false} path="" redirect="/login">
      <Navigate replace to="/dashboard" />
    </ProtectedRoute>
   */
}
const AppRouter: React.FC = (): React.ReactElement => (
  <Routes>
    <Route path="/login" element={<Login />} />
    <Route path="/dashboard/*" element={<Dashboard />} />
  </Routes>
);

export default AppRouter;
