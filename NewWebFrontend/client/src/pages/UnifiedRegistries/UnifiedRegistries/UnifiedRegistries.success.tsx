import React, { useState } from 'react';

import Table from '@components/Table';

import { TUnifiedRegistriesSuccessProps } from './UnifiedRegistries.types';

import { TGetAllUnifiedRegistriesSuccess } from '@APIs/unifiedRegistry/unifiedRegistry.types';

import HighlightedValue from '@secureailabs/web-ui/components/HighlightedValue';

import Marker from '@secureailabs/web-ui/components/Marker';

import Margin from '@secureailabs/web-ui/components/Margin';
import Text from '@secureailabs/web-ui/components/Text';

const UnifiedRegistrySuccess: React.FC<TUnifiedRegistriesSuccessProps> = ({
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
          value: { Name: string, Image: string; Description: string, owner_name: string };
        }) => {
          const { Name, Image, Description, owner_name } = value;
          return (
            <div className="unified-registry-preview">
              <img src={Image} />
              <div className="unified-registry-preview__name_and_def">
                <Text fontSize='1.2rem' fontWeight='600'>{Name}</Text>
                <Text fontSize='1.2rem' fontWeight='400'>{Description}</Text>
                <Marker>{owner_name == 'Sallie Director' ? 'Data Owner' : 'Data User'}</Marker>
              </div>
            </div>
          );
        },
      },
      {
        Header: 'Owner',
        accessor: 'owner_org',
        width: 100,
      },
      {
        Header: 'Date Created',
        accessor: 'CreatedAt',
        width: 100,
        Cell: ({ value }: { value: Date }) => {
          return value.toLocaleDateString(undefined, {year: 'numeric', month: 'long', day: 'numeric'});
        },
      },
      {
        Header: 'No. Of Data Owners',
        accessor: 'NumberOfDataOwner',
        width: 100,
        Cell: ({ value }: { value: number }) => {
          return <HighlightedValue>{value.toString()}</HighlightedValue>;
        },
      },

      {
        Header: 'No. Of Patients',
        accessor: 'NumberOfPatients',
        width: 200,
        Cell: ({ value }: { value: number }) => {
          return <HighlightedValue>{value.toString()}</HighlightedValue>;
        },
      },
    ],
    []
  );
  const parsedData = Object.entries(
    getAllUnifiedRegistriesData.UnifiedRegistries
  ).map(([key, value]) => {
    return {
      key,
      Registry: {
        Name: value.Name,
        Image: value.Image,
        Description: value.Description,
        owner_name: value.owner_name,
      },
      ...value,
    };
  });
  return (
    <>
      <Margin size={5} />
      <Table
        base_url="/dashboard/registries"
        id_accessor="key"
        columns={columns}
        data={parsedData}
      />
    </>
  );
};

export default UnifiedRegistrySuccess;
