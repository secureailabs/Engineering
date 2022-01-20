import React from 'react';

import NavBar from '@components/NavBar';
import DashboardRouter from '@routes/Dashboard.routes';

const Dashboard = () => {
  return (
    <>
      <NavBar />
      <DashboardRouter />
    </>
  );
};

export default Dashboard;
