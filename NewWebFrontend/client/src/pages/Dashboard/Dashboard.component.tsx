import React from 'react';

import { FaServer } from 'react-icons/fa';
import { HiOutlineDesktopComputer } from 'react-icons/hi';
import {
  MdDashboard, MdHelpOutline,
  MdLaunch,
  MdLogout, MdOutlineDocumentScanner,
  MdOutlinePeopleAlt, MdSettings, MdSystemUpdateAlt, MdViewColumn
} from 'react-icons/md';

import DashboardRouter from '@routes/Dashboard.routes';

import Header from '@secureailabs/web-ui/components/Header';
import Sidebar from '@secureailabs/web-ui/layout/Sidebar';

import newLogo from '@assets/newLogo.png';
import default_profile_image from '@assets/user.png';

import BreadcrumbRoutes from '@routes/Breadcrumbs/breadcrumbs.routes';

import { TDashboardProps } from './Dashboard.types';

const Dashboard: React.FC<TDashboardProps> = ({ userData, logoutMutationFunction }) => {
  let primary: any[] = [
    { text: 'Dashboard', Icon: MdDashboard, link: '/dashboard', exact: true },
    { text: 'Datasets', Icon: MdViewColumn, link: '/dashboard/datasets' },
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
    primary = primary.concat([
      {
        text: 'Computational Resources',
        Icon: HiOutlineDesktopComputer,
        link: '/dashboard/computational-resources',
      },
      {
        text: 'Unified Registries',
        Icon: FaServer,
        link: '/dashboard/registries',
      },
      {
      text: 'Launch Notebook',
      Icon: MdLaunch,
      onClick: () => {
        // @ts-ignore
        window.location.href = import.meta.env.VITE_PUBLIC_JUPYTER_URL || "http://52.152.225.54:8080/lab?token=fa8dfcf5a8cfd55402f687698847adabced336cd0423172c"
        },
      },
      {
      text: 'Launch Demo',
      Icon: MdLaunch,
      onClick: () => {
        // @ts-ignore
        window.location.href = "http://20.124.39.153:8501/demo_1"
        },
      },
    ])

    secondary = [
    {
      text: 'Downloads',
      Icon: MdSystemUpdateAlt,
      link: '/dashboard/downloads'
    },
    {
      text: 'Documentation',
      Icon: MdOutlineDocumentScanner,
      link: '/dashboard/documentation'
    },
    {
      text: 'Settings',
      Icon: MdSettings,
      link: '/dashboard/settings',
    },
    {
      text: 'My Organization',
      Icon: MdOutlinePeopleAlt,
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
