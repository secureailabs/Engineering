import React, { useState } from 'react';

import Table from '@components/Table';

import { TDatasetsSuccessProps } from './Datasets.types';

import Text from '@secureailabs/web-ui/components/Text';

import faker from 'faker';

const DatasetsSuccess: React.FC<TDatasetsSuccessProps> = ({
  getAllDatasetsData,
}) => {
  console.log(getAllDatasetsData);
  const columns = React.useMemo(
    () => [
      {
        Header: 'Name',
        accessor: 'DatasetName',
        width: 300,
      },
      // {
      //   Header: 'No. of Versions',
      //   accessor: 'Versions',
      //   width: 300,
      //   Cell: ({ value }: { value: Record<string, any> }) => (
      //     <Text color="primary">{Object.keys(value).length}</Text>
      //   ),
      // },
      {
        Header: 'Publish Date',
        accessor: 'PublishDate',
        width: 300,
      },

      {
        Header: 'Keywords',
        accessor: 'Keywords',

        width: 200,
      },
      {
        Header: 'Dataset Owner',
        accessor: 'DatasetOwners',
        width: 200,
      },
    ],
    []
  );

  const parsedData = Object.entries(getAllDatasetsData)
    .map(([key, value]) => {
      return {
        key,
        ...value,
        PublishDate: faker.date.recent(3).toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        }),
      };
    })
    .sort((elem1, elem2) => elem1.PublishDate.localeCompare(elem2.PublishDate));
  return (
    <>
      <Table
        base_url="/dashboard/datasets"
        id_accessor="key"
        columns={columns}
        data={parsedData}
      />
    </>
  );
};

export default DatasetsSuccess;
