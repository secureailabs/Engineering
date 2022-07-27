import kca_logo from '@assets/kca.png';
import preview from '@assets/preview.png';

import Datasets from '@APIs/dataset/dataset.data';

import faker from 'faker';

export const demo_data = {
  UnifiedRegistries: {
    'uuid1': {
      ID: 'uuid1',
      Name: 'KCA Consortium',
      Description:
        "The Kidney Cancer Association Research Consortium is the first consortium of researchers and hospitals creating a Unified Patient Registry for advancing medical research for Kidney Cancer.",
      Image: kca_logo,
      NumberOfDataOwner: 7,
      NumberOfPatients: 25639,
      CreatedAt: faker.date.recent(2),
      UpdateAt: faker.date.recent(1),
      Datasets: Datasets.datasets,

      owner_name: 'Sallie',
      owner_org: 'KCA',
      owner_org_id: 'uuid1'
    },
    'uuid2': {
      ID: 'uuid2',
      Name: 'Pancreatic Cancer Research Consortium',
      Description:
        "The Pancreatic Cancer Research Consortium connects datasets from the leading pancreatic cancer treatment centers with academic and industry researchers. ",
      Image: preview,
      NumberOfDataOwner: 5,
      NumberOfPatients: 15287,
      CreatedAt: faker.date.recent(2),
      UpdateAt: faker.date.recent(1),
      Datasets: Datasets.datasets,

      owner_name: 'Robert',
      owner_org: 'PCR',
      owner_org_id: 'uuid2'
    },
  },
};
