import React from 'react';

import {
  MdDashboard,
  MdViewColumn,
  MdSettings,
  MdHelpOutline,
  MdLaunch,
  MdLogout,
} from 'react-icons/md';
import { IoMdDocument } from 'react-icons/io';
import { HiOutlineDesktopComputer } from 'react-icons/hi';
import { FaServer } from 'react-icons/fa';

import DashboardRouter from '@routes/Dashboard.routes';

import Sidebar from '@secureailabs/web-ui/layout/Sidebar';
import Header from '@secureailabs/web-ui/components/Header';

import default_profile_image from '@assets/user.png';
import newLogo from '@assets/newLogo.png';

import BreadcrumbRoutes from '@routes/Breadcrumbs/breadcrumbs.routes';

import { TDashboardProps } from './Dashboard.types';

const Dashboard: React.FC<TDashboardProps> = ({ userData, logoutMutationFunction }) => {
  let primary: any[] = [
    { text: 'Dashboard', Icon: MdDashboard, link: '/dashboard', exact: true },
    { text: 'Datasets', Icon: MdViewColumn, link: '/dashboard/datasets' },
    {
      text: 'Virtual Machines',
      Icon: HiOutlineDesktopComputer,
      link: '/dashboard/virtual-machines',
    }
  ];
  let secondary: any[] = [
    {
      text: 'Logout',
      Icon: MdLogout,
      onClick: () => {
        logoutMutationFunction()
      },
    },
  ];

  if (localStorage.getItem('mode') == 'demo') {
    primary = primary.concat([{
      text: 'Launch Notebook',
      Icon: MdLaunch,
      onClick: () => {
        // @ts-ignore
        window.location.href = import.meta.env.VITE_PUBLIC_JUPYTER_URL || "http://52.152.225.54:8080/lab?token=fa8dfcf5a8cfd55402f687698847adabced336cd0423172c"
      },
    },
    {
      text: 'Unified Registries',
      Icon: FaServer,
      link: '/dashboard/registries',
    }])

    secondary = [{
      text: 'Settings',
      Icon: MdSettings,
      link: '/dashboard/settings',
    },
    {
      text: 'My Organization',
      Icon: MdSettings,
      link: '/dashboard/my-organization',
    },
    {
      text: 'Help',
      Icon: MdHelpOutline,
      link: '/dashboard/help',
    }].concat(secondary)
  }

  return (
    <>
      <Sidebar primary={primary} secondary={secondary} logo={newLogo}>
        <div className="standard-grid-row">
          <Header
            search={() => { }}
            username={userData?.name}
            profile_image={default_profile_image}
            organization={userData?.organization.name}
          />
          <div>
            <BreadcrumbRoutes />
            <DashboardRouter />
          </div>
        </div>
      </Sidebar>
    </>
  );
};

export default Dashboard;
