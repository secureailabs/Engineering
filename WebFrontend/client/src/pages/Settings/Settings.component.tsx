import React from 'react';

import type { TSettings } from './Settings.types';

import accessRightsNumberToString from '@utils/accessRightsNumberToString';

import UpdateUser from '@components/Settings/UpdateUser';
import UpdatePassword from '@components/Settings/UpdatePassword';
import Title from '@components/Title';
// import UpdateAccessRights from '@components/Settings/UpdateAccessRights';

import InfoDisplay from '@components/InfoDisplay';
import {
  removeValues,
  reorganizeObject,
  convertObjectToArray,
  reorganizeArray,
  changeArrayKeys,
} from '@components/InfoDisplay/InfoDisplay.utils';

const Settings: React.FC<TSettings> = ({ userData }) => {
  console.log(userData);

  if (userData) {
    let newData: Record<string, any> = userData;
    let arrayData = convertObjectToArray(newData);
    arrayData = reorganizeArray(arrayData, [
      'Username',
      'Title',
      'Email',
      'AccessRights',
    ]);
    arrayData = changeArrayKeys(arrayData, [
      'Name',
      'Job Title',
      'Email',
      'Access Rights',
    ]);
    arrayData[3][1] = accessRightsNumberToString(arrayData[3][1]);
    return (
      <>
        <Title>Settings</Title>
        <UpdateUser />
        <UpdatePassword />
        {/* <InfoDisplay title="Settings" data={arrayData} /> */}
      </>
    );
  }
  return <>Unable to fetch user data</>;
};

export default Settings;
