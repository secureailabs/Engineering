import React from 'react';
import TimeAgo from 'javascript-time-ago';

import en from 'javascript-time-ago/locale/en.json';
TimeAgo.addLocale(en);
const timeAgo = new TimeAgo('en');

import Feed from '@secureailabs/web-ui/components/Feed';

import GridLayout from 'react-grid-layout';

import StandardContent from '@secureailabs/web-ui/components/StandardContent';
import Stats from '@secureailabs/web-ui/components/Stats';
import feed_image1 from '@secureailabs/web-ui/assets/feed1.jpeg';
import feed_image2 from '@secureailabs/web-ui/assets/feed2.jpeg';

import { FaUsers } from 'react-icons/fa';
const CustomizableDashboard = () => {
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
    { i: 'b', x: 8, y: 5, w: 2, h: 8 },
    { i: 'c', x: 8, y: 0, w: 2, h: 7 },
  ];

  const feed1 = {
    title: 'Feed',
    secondary: 'Show all',
    feed: [
      {
        title:
          'Vanderbilt University published a new version of the ‘KCA consortium data set',
        description:
          "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s",
        image: feed_image1,
        date: timeAgo.format(new Date()),
      },
      {
        title:
          'Mayo Clinic was added to the KCA Research Consortium as a Data Owner',
        description:
          "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s",
        image: feed_image2,

        date: timeAgo.format(new Date()),
      },
    ],
  };
  const feed2 = {
    title: 'Data User Activity',
    secondary: 'Show all',
    feed: [
      {
        title: 'Lorem Ipsum',
        description: 'performs data updates on lorem ipsum',

        date: timeAgo.format(new Date()),
      },
      {
        title: 'Lorem Ipsum',
        description: 'performs data updates on lorem ipsum',
        date: timeAgo.format(new Date()),
      },
    ],
  };

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
          <Feed containerHeight={true} {...feed1} />
        </div>
        <div key="b">
          <Feed containerHeight={true} {...feed2} />
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
};

export default CustomizableDashboard;
