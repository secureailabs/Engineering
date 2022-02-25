import React from 'react';
import TimeAgo from 'javascript-time-ago';

import en from 'javascript-time-ago/locale/en.json';
TimeAgo.addLocale(en);
const timeAgo = new TimeAgo('en');

import PatientSummary from '@components/PatientSummary';

import Feed from '@components/Feed';

import GridLayout from 'react-grid-layout';

import StandardContent from '@secureailabs/web-ui/components/StandardContent';
import Stats from '@secureailabs/web-ui/components/Stats';

import { FaUsers } from 'react-icons/fa';
import { IUserData } from '@redux/user/user.typeDefs';

const CustomizableDashboard: React.FC<{ userData: IUserData }> = ({
  userData,
}) => {
  const stats = [
    {
      title: 'No. of Data Users',
      Icon: FaUsers,
      value: '7',
    },
    {
      title: 'No. of Data Users',
      Icon: FaUsers,
      value: '7',
    },
  ];

  const layout = [
    { i: 'a', x: 0, y: 0, w: 8, h: 5 },
    { i: 'b', x: 0, y: 5, w: 5, h: 6 },
    { i: 'c', x: 8, y: 0, w: 2, h: 7 },
  ];
  console.log(userData);
  if (userData?.AccessRights === 6) {
    return (
      <StandardContent title="Dashboard">
        <GridLayout
          className="layout"
          layout={layout}
          cols={12}
          width={1400}
          rowHeight={50}
        >
          <div key="a">
            <Feed containerHeight={true} limit={2} />
          </div>
          <div key="b">
            <PatientSummary />
          </div>
          <div key="c">
            <Stats
              title="Summary of Membership"
              containerHeight={true}
              stats={stats}
            />
          </div>
        </GridLayout>
      </StandardContent>
    );
  } else {
    return (
      <StandardContent title="Dashboard">
        <Feed limit={5} />
      </StandardContent>
    );
  }
};

export default CustomizableDashboard;
