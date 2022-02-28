import * as React from 'react';
import { Navigate, Routes, Route } from 'react-router-dom';
import Dashboard from '@pages/Dashboard';
import Login from '@pages/Login';
import Signup from '@pages/Signup';

import ProtectedRoute from './ProtectedRoute';
import UnProtectedRoute from './UnProtectedRoute';
<<<<<<< HEAD
=======

{
  /*
      *
      *
    <UnProtectedRoute exact path="/login" redirect="/dashboard">
      <Login />
    </UnProtectedRoute>
>>>>>>> b41571f88d730ba2c67b769937b1ee6251f27ee9

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
    <Route path="*" element={<Navigate to="/login" />}/>
  </Routes>
);

export default AppRouter;
