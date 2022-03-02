//@ts-nocheck
import * as React from 'react';
import { Navigate, Routes, Route } from 'react-router-dom';
import Dashboard from '@pages/Dashboard';
import Login from '@pages/Login';
import Signup from '@pages/Signup';

import ProtectedRoute from './ProtectedRoute';
import UnProtectedRoute from './UnProtectedRoute';

const AppRouter: React.FC = (): React.ReactElement => (
  <Routes>
    <Route path="/" element={<Navigate replace to="/login" />} />
    <Route
      path="/login"
      element={
        <UnProtectedRoute redirect="/dashboard">
          <Login />
        </UnProtectedRoute>
      }
    />
    <Route path="/dashboard/*" element={<Dashboard />} />
    <Route path="*" element={<Navigate to="/login" />} />
  </Routes>
);

export default AppRouter;
