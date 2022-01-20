import * as React from 'react';
import { Redirect, Switch } from 'react-router-dom';

import ProtectedRoute from './ProtectedRoute';
import RestrictedRoute from './RestrictedRoute';
import DatasetList from '@pages/Datasets';
import DigitalContracts from '@pages/DigitalContracts';
import MainMenu from '@pages/MainMenu';
import SettingsPage from '@pages/Settings';
import AccountManager from '@pages/AccountManager';
import Organization from '@pages/Organization';
import AzureTemplatesManager from '@pages/AzureTemplatesManager';
import UnderConstruction from '@pages/UnderConstruction';
import VirtualMachines from '@pages/VirtualMachines';

const DashboardRouter: React.FC = (): React.ReactElement => (
  <Switch>
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

    {/* Handle default routes */}
    <ProtectedRoute exact={false} path="" redirect="/login">
      <MainMenu />
    </ProtectedRoute>
  </Switch>
);

export default DashboardRouter;
