import React from 'react';

import NavBar from '@components/NavBar';
import DashboardRouter from '@routes/Dashboard.routes';
import Sidebar from '@secureailabs/web-ui/layout/Sidebar';
import Header from '@secureailabs/web-ui/components/Header';
import Footer from '@secureailabs/web-ui/components/Footer';
import {
  MdDashboard,
  MdViewColumn,
  MdSettings,
  MdHelpOutline,
  MdLogout,
} from 'react-icons/md';

import { IoMdDocument } from 'react-icons/io';

import { HiOutlineDesktopComputer } from 'react-icons/hi';

import { CgTemplate } from 'react-icons/cg';

import default_profile_image from '@assets/user.png';

import newLogo from '@assets/newLogo.png';

import { FaServer } from 'react-icons/fa';
const Dashboard = () => {
  const primary = [
    { text: 'Dashboard', Icon: MdDashboard, link: '/dashboard' },
    { text: 'Datasets', Icon: MdViewColumn, link: '/dashboard/datasets' },
    {
      text: 'Digital Contracts',
      Icon: IoMdDocument,
      link: '/dashboard/digital-contracts',
    },
    {
      text: 'Virtual Machines',
      Icon: HiOutlineDesktopComputer,
      link: '/dashboard/virtual-machines',
    },
    {
      text: 'Azure Templates Manager',
      Icon: CgTemplate,
      link: '/dashboard/azure-templates',
    },
    {
      text: 'Unified Registries',
      Icon: FaServer,
      link: '/dashboard/registries',
    },
  ];
  const secondary = [
    {
      text: 'Settings',
      Icon: MdSettings,
      link: '/dashboard/settings',
    },
    {
      text: 'Help',
      Icon: MdHelpOutline,
      link: '/dashboard/help',
    },
    {
      text: 'Logout',
      Icon: MdLogout,
      onClick: () => {},
    },
  ];

  // <DashboardRouter />
  return (
    <>
      <Sidebar primary={primary} secondary={secondary} logo={newLogo}>
        <div className="standard-grid-row">
          <Header
            search={() => {}}
            username="User_name"
            profile_image={default_profile_image}
            organization="Mayo Clinic"
          />
          <DashboardRouter />
          <Footer />
        </div>
      </Sidebar>
    </>
  );
};

export default Dashboard;
