import React, { ReactElement } from 'react';
import { useHistory } from 'react-router';

import { GrOrganization } from 'react-icons/gr';

import { SiMicrosoftazure } from 'react-icons/si';

import {
  HiViewBoards,
  HiPencil,
  HiDesktopComputer,
  HiUsers,
  HiCog,
  HiQuestionMarkCircle,
} from 'react-icons/hi';

import Tile from '@components/Tile/tile.component';
import { IMainMenu } from './MainMenu.types';

const MainMenu: React.FC<IMainMenu> = ({ userData }): ReactElement => {
  const history = useHistory();
  return (
    <div className="mainmenu">
      <div className="mainmenu__title">Main Menu</div>
      <div className="mainmenu__tilecontainer">
        <Tile
          Icon={HiViewBoards}
          title="Datasets"
          description="Browse available datasets and request access to them."
          onClick={() => history.push('/dashboard/availabledatasets')}
        />
        <Tile
          Icon={HiPencil}
          title="Digital Contracts"
          description="Approve, activate and see the status of your digital contracts."
          onClick={() => history.push('/dashboard/digitalcontracts')}
        />
        <Tile
          Icon={HiDesktopComputer}
          title="Secure Computation Nodes"
          description="Manage your Secure Computation Nodes"
          onClick={() => history.push('/dashboard/virtualmachines')}
        />
        {userData?.AccessRights == 1 && (
          <>
            <Tile
              Icon={HiUsers}
              title="Users"
              description="Create new users, and update permissions."
              onClick={() => history.push('/dashboard/admin')}
            />
            <Tile
              Icon={GrOrganization}
              title="Organization"
              description="Update organization information."
              onClick={() => history.push('/dashboard/organization')}
            />
            <Tile
              Icon={SiMicrosoftazure}
              title="Azure Templates Manager"
              description="Create, update and delete Azure templates."
              onClick={() => history.push('/dashboard/azure')}
            />
          </>
        )}
        <Tile
          Icon={HiCog}
          title="Settings"
          description="Change your settings."
          onClick={() => history.push('/dashboard/settings')}
        />
        <Tile
          Icon={HiQuestionMarkCircle}
          title="Help"
          description="Get help from SAIL support."
          onClick={() => history.push('/dashboard/help')}
        />
      </div>
    </div>
  );
};

export default MainMenu;
