import React, { useState } from 'react';

import Table from '@components/Table';

import { TUnifiedRegistrysSuccessProps } from './UnifiedRegistries.types';

import { TGetAllUnifiedRegistriesSuccess } from '@redux/unifiedRegistry/unifiedRegistry.types';

import TableFilter from '@secureailabs/web-ui/components/TableFilter';

import HighlightedValue from '@secureailabs/web-ui/components/HighlightedValue';

import Margin from '@secureailabs/web-ui/components/Margin';
import TimeAgo from 'javascript-time-ago';
import Text from '@secureailabs/web-ui/components/Text';

import en from 'javascript-time-ago/locale/en.json';
TimeAgo.addLocale(en);
const timeAgo = new TimeAgo('en');

const UnifiedRegistrySuccess: React.FC<TUnifiedRegistrysSuccessProps> = ({
  getAllUnifiedRegistriesData,
}) => {
  const columns = React.useMemo(
    () => [
      {
        Header: 'Registry',
        accessor: 'Registry',
        width: 100,
        Cell: ({
          value,
        }: {
          value: { Image: string; Description: string };
        }) => {
          const { Image, Description } = value;
          return (
            <div className="unified-registry-preview">
              <img src={Image} />
              <Text>{Description}</Text>
            </div>
          );
        },
      },
      {
        Header: 'CreatedDate',
        accessor: 'CreatedAt',
        width: 100,
        Cell: ({ value }: { value: Date }) => {
          return timeAgo.format(value);
        },
      },
      {
        Header: 'No. of data owner',
        accessor: 'NumberOfDataOwner',
        width: 100,
        Cell: ({ value }: { value: number }) => {
          return <HighlightedValue>{value}</HighlightedValue>;
        },
      },

      {
        Header: 'No. of patients',
        accessor: 'NumberOfPatients',
        width: 200,
        Cell: ({ value }: { value: number }) => {
          return <HighlightedValue>{value}</HighlightedValue>;
        },
      },
    ],
    []
  );
  console.log(getAllUnifiedRegistriesData);
  const parsedData = Object.entries(
    getAllUnifiedRegistriesData.UnifiedRegistries
  ).map(([key, value]) => {
    return {
      key,
      Registry: {
        Image: value.Image,
        Description: value.Description,
      },
      ...value,
    };
  });
  console.log(parsedData);
  return (
    <>
      <Margin size={5} />
      <Table
        base_url="/dashboard/virtual-machines"
        id_accessor="key"
        columns={columns}
        data={parsedData}
      />
    </>
  );
};

export default UnifiedRegistrySuccess;
