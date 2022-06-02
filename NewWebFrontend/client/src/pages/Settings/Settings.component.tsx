import React from 'react';

import type { TSettings } from './Settings.types';

import accessRightsNumberToString from '@utils/accessRightsNumberToString';

import StandardContent from '@secureailabs/web-ui/components/StandardContent';
import Card from '@secureailabs/web-ui/components/Card';
import Text from '@secureailabs/web-ui/components/Text';
import Button from '@secureailabs/web-ui/components/Button';
import Margin from '@secureailabs/web-ui/components/Margin';
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

  // if (userData) {
  //   let newData: Record<string, any> = userData;
  //   let arrayData = convertObjectToArray(newData);
  //   arrayData = reorganizeArray(arrayData, [
  //     'Username',
  //     'Title',
  //     'Email',
  //     'AccessRights',
  //   ]);
  //   arrayData = changeArrayKeys(arrayData, [
  //     'Name',
  //     'Job Title',
  //     'Email',
  //     'Access Rights',
  //   ]);
  //   arrayData[3][1] = accessRightsNumberToString(arrayData[3][1]);
  //   return <></>;
  // }
  return (
    <>
      <StandardContent title="Settings">
        <>
          <Card primaryText="My Profile">
            <div className="my-profile">
              <Text>
                Lorem Ipsum is simply dummy text of the printing and typesetting
                industry. Lorem Ipsum has been the industry&apos;s standard
                dummy text ever since the 1500s, when an unknown.
              </Text>
              <Button full={false} button_type="secondary">
                Edit My Profile
              </Button>
            </div>
          </Card>

          <Margin size={8} />
          <Card primaryText="Users">
            <div className="my-profile">
              <Text>
                Lorem Ipsum is simply dummy text of the printing and typesetting
                industry. Lorem Ipsum has been the industry&apos;s standard
                dummy text ever since the 1500s, when an unknown.
              </Text>
              <Button full={false} button_type="secondary">
                Add User
              </Button>
            </div>
          </Card>
          <Margin size={8} />
          <Card primaryText="My Organization">
            <div className="my-profile">
              <Text>
                Lorem Ipsum is simply dummy text of the printing and typesetting
                industry. Lorem Ipsum has been the industry&apos;s standard
                dummy text ever since the 1500s, when an unknown.
              </Text>
              <Button full={false} button_type="secondary">
                Edit My Organization
              </Button>
            </div>
          </Card>
        </>
      </StandardContent>
    </>
  );
};

export default Settings;
