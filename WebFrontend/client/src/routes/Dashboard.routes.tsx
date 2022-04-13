import * as React from 'react';
import { Routes, Route } from 'react-router-dom';

import ProtectedRoute from './ProtectedRoute';
import UnProtectedRoute from './UnProtectedRoute';
import RestrictedRoute from './RestrictedRoute';
import Datasets from '@pages/Datasets/Datasets';
import Dataset from '@pages/Datasets/Dataset';
import DigitalContracts from '@pages/DigitalContracts/DigitalContracts';
import DigitalContract from '@pages/DigitalContracts/DigitalContract';
import MainMenu from '@pages/MainMenu';
import SettingsPage from '@pages/Settings';
import Organization from '@pages/Organization';
import UnderConstruction from '@pages/UnderConstruction';
import VirtualMachines from '@pages/VirtualMachines/VirtualMachines';
import VirtualMachine from '@pages/VirtualMachines/VirtualMachine';
import UnifiedRegistries from '@pages/UnifiedRegistries/UnifiedRegistries';
import UnifiedRegistry from '@pages/UnifiedRegistries/UnifiedRegistry';
import CustomizableDashboard from '@components/CustomizableDashboard';
import DatasetVersion from '@pages/Datasets/DatasetVersion';
import ViewOrganization from '@pages/ViewOrganization';

const DashboardRouter: React.FC = (): React.ReactElement => (
  <Routes>
    <Route
      path="/registries"
      element={
        <ProtectedRoute redirect="/login">
          <UnifiedRegistries />
        </ProtectedRoute>
      }
    />
    <Route
      path="/registries/:id"
      element={
        <ProtectedRoute redirect="/login">
          <UnifiedRegistry />
        </ProtectedRoute>
      }
    />

    <Route
      path="/"
      element={
        <ProtectedRoute redirect="/login">
          <CustomizableDashboard />
        </ProtectedRoute>
      }
    />
    <Route
      path="/digital-contracts"
      element={
        <ProtectedRoute redirect="/login">
          <DigitalContracts />
        </ProtectedRoute>
      }
    />
    <Route
      path="/digital-contracts/:id"
      element={
        <ProtectedRoute redirect="/login">
          <DigitalContract />
        </ProtectedRoute>
      }
    />
    <Route
      path="/virtual-machines"
      element={
        <ProtectedRoute redirect="/login">
          <VirtualMachines />
        </ProtectedRoute>
      }
    />
    <Route
      path="/virtual-machines/:id"
      element={
        <ProtectedRoute redirect="/login">
          <VirtualMachine />
        </ProtectedRoute>
      }
    />
    <Route
      path="/datasets"
      element={
        <ProtectedRoute redirect="/login">
          <Datasets />
        </ProtectedRoute>
      }
    />
    <Route
      path="/datasets/:id"
      element={
        <ProtectedRoute redirect="/login">
          <Dataset />
        </ProtectedRoute>
      }
    />
    <Route
      path="/datasets/:id/:version"
      element={
        <ProtectedRoute redirect="/login">
          <DatasetVersion />
        </ProtectedRoute>
      }
    />
    <Route
      path="/organizations/:id"
      element={
        <ProtectedRoute redirect="/login">
          <ViewOrganization />
        </ProtectedRoute>
      }
    />
    <Route
      path="/settings"
      element={
        <ProtectedRoute redirect="/login">
          <SettingsPage />
        </ProtectedRoute>
      }
    />
    <Route
      path="/my-organization"
      element={
        <ProtectedRoute redirect="/login">
          <Organization />
        </ProtectedRoute>
      }
    />
  </Routes>
);

export default DashboardRouter;
