import React from 'react';
import { Link } from 'react-router-dom';

import LargeLogo from '@components/LargeLogo';
import accessRightsNumberToString from '@utils/accessRightsNumberToString';

import { TNavBarProps } from './NavBar.types';

const NavBar: React.FC<TNavBarProps> = ({ signOutStart, userData }) => {
  // console.log('--------------------------------')
  // console.log(userData)
  // console.log(userData?.Username)
  return (
    <div className="navbar">
      <LargeLogo />
      <div className='navbar__userinfo'>
        {userData?.Email} - {userData?.Username}, {userData?.Title}, {userData?.OrganizationName} - {userData && accessRightsNumberToString(userData?.AccessRights)}
      </div>
      <div className="navbar__linksright">
        <Link className="navbar__link" to="/dashboard">
          Main Menu
        </Link>
        <Link onClick={signOutStart} className="navbar__link" to="/login">
          Log Out
        </Link>
      </div>
    </div>
  );
};

export default NavBar;
