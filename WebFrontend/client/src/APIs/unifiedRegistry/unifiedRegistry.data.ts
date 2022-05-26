import kca_logo from '@assets/kca.png';

import Datasets from '@APIs/dataset/dataset.data';

import faker from 'faker';

export const demo_data = {
  UnifiedRegistries: {
    uuid1: {
      ID: 'uuid1',
      Name: 'string',
      Description:
        "KCA Consortium RegistryLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s ....",
      Image: kca_logo,
      NumberOfDataOwner: 7,
      NumberOfPatients: 29,
      CreatedAt: faker.date.recent(2),
      UpdateAt: faker.date.recent(1),
      Datasets: Datasets.Datasets,
    },
  },
};
