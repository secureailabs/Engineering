import React from 'react';
import ribbon2 from '@assets/pink_ribbon2.jpeg';
import ribbon from '@assets/pink_ribbon.jpeg';
import mayo from '@assets/mayo.jpeg';
import boob from '@assets/cancer_scan.jpeg';
import stop_cancer from '@assets/stop_cancer.jpeg';
import { Link } from 'react-router-dom';
import faker from 'faker';
export const demo_data = {
  Feeds: {
    uuid1: {
      ID: 'uuid1',
      Title: (
        <p>
          <Link to="/dashboard/organizations/1">Cancer Research Hospital</Link> published a{' '}
          <Link to="/dashboard/datasets/uuid1/uuid1_1">new version</Link> of the{' '}
          <Link to="/dashboard/registries/uuid1">KCA consortium</Link> data set
        </p>
      ),
      Description: '',
      avatar: 'Cancer Research Hospital',
      avatar_color: '#FF0000',
      CreatedAt: faker.date.recent(3),
      UpdatedAt: new Date(),
    },
    uuid2: {
      ID: 'uuid2',
      Title:
        'Mayo Clinic was added to the KCA Research Consortium as a Data Owner',
      Description: '',
      Image: mayo,

      CreatedAt: faker.date.recent(3),
      UpdatedAt: new Date(),
    },
    uuid3: {
      ID: 'uuid3',
      Title:
        'Vanderbilt University published a new version of the ‘KCA consortium data set',
      Description:
        "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s",
      Image: boob,
      CreatedAt: faker.date.recent(3),
      UpdatedAt: new Date(),

      Link: '/dashboard/datasets/uuid1',
    },
    uuid4: {
      ID: 'uuid4',
      Title:
        'Mayo Clinic was added to the KCA Research Consortium as a Data Owner',
      Description: '',
      Image: stop_cancer,
      CreatedAt: faker.date.recent(3),
      UpdatedAt: new Date(),

      Link: '/dashboard/datasets/uuid1',
    },
    uuid5: {
      ID: 'uuid5',
      Title:
        'Vanderbilt University published a new version of the ‘KCA consortium data set',
      Description: '',
      Image: ribbon,

      CreatedAt: faker.date.recent(3),
      UpdatedAt: new Date(),

      Link: '/dashboard/datasets/uuid1',
    },
  },
};
