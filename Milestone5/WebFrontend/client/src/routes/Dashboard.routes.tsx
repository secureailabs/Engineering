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
import AccountManager from '@pages/AccountManager';
import Organization from '@pages/Organization';
import AzureTemplates from '@pages/AzureTemplates/AzureTemplatesManager';
import AzureTemplate from '@pages/AzureTemplates/AzureTemplate';
import UnderConstruction from '@pages/UnderConstruction';
import VirtualMachines from '@pages/VirtualMachines/VirtualMachines';
import VirtualMachine from '@pages/VirtualMachines/VirtualMachine';
import UnifiedRegistries from '@pages/UnifiedRegistries/UnifiedRegistries';
import CustomizableDashboard from '@components/CustomizableDashboard';
import DatasetVersion from '@pages/Datasets/DatasetVersion';
{
  /*
       *

    <ProtectedRoute
      exact={false}
      path="/dashboard/virtualmachines"
      redirect="/login"
    >
      <VirtualMachines />
    </ProtectedRoute>
    <ProtectedRoute
      exact={false}
      path="/dashboard/digitalcontracts"
      redirect="/login"
    >
      <DigitalContracts />
    </ProtectedRoute>
    <ProtectedRoute
      exact={false}
      path="/dashboard/organization"
      redirect="/login"
    >
      <Organization />
    </ProtectedRoute>

    <ProtectedRoute
      exact={false}
      path="/dashboard/availabledatasets"
      redirect="/login"
    >
      <DatasetList />
    </ProtectedRoute>

    <RestrictedRoute
      exact={false}
      path="/dashboard/azure"
      redirect="/login"
      requiredAccessRights={1}
    >
      <AzureTemplatesManager />
    </RestrictedRoute>

    <RestrictedRoute
      exact={false}
      path="/dashboard/admin"
      redirect="/login"
      requiredAccessRights={1}
    >
      <AccountManager />
    </RestrictedRoute>

    <ProtectedRoute exact={false} path="/dashboard/settings" redirect="/login">
      <SettingsPage />
    </ProtectedRoute>

    <ProtectedRoute exact={false} path="/dashboard/help" redirect="/login">
      <UnderConstruction />
    </ProtectedRoute>

    <UnProtectedRoute exact={false} path="" redirect="/login">
      <MainMenu />
    </UnProtectedRoute>
    */
}
const DashboardRouter: React.FC = (): React.ReactElement => (
  <Routes>
    <Route
      path="/azure-templates"
      element={
        <ProtectedRoute redirect="/login">
          <AzureTemplates />
        </ProtectedRoute>
      }
    />
    <Route
      path="/azure-templates/:id"
      element={
        <ProtectedRoute redirect="/login">
          <AzureTemplate />
        </ProtectedRoute>
      }
    />

    <Route
      path="/registries"
      element={
        <ProtectedRoute redirect="/login">
          <UnifiedRegistries />
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
      path="/settings"
      element={
        <ProtectedRoute redirect="/login">
          <SettingsPage />
        </ProtectedRoute>
      }
    />
  </Routes>
);

export default DashboardRouter;
