import React, { useState } from 'react';

import Table from '@components/Table';

import { TDigitalContractsSuccessProps } from './DigitalContracts.types';

import TableFilter from '@secureailabs/web-ui/components/TableFilter';

import Margin from '@secureailabs/web-ui/components/Margin';

import getDCStage from '@utils/getDCStage';

import getPartnerOrg from '@utils/getPartnerOrg';

import faker from 'faker';

const DigitalContractsSuccess: React.FC<TDigitalContractsSuccessProps> = ({
  getAllDigitalContractsData,
  userData,
}) => {
  const columns = React.useMemo(
    () => [
      {
        Header: 'Title',
        accessor: 'Title',
        width: 300,
      },
      {
        Header: 'Dataset',
        accessor: 'DatasetName',
        width: 300,
      },
      {
        Header: 'Partner Organization',
        accessor: 'PartnerOrg',
        width: 300,
      },

      {
        Header: 'Last Activity',
        accessor: 'LastActivity',
        Cell: ({ value }: { value: number }) =>
          faker.date.recent(1).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
            second: 'numeric',
          }),
        width: 200,
      },
      {
        Header: 'Provisioning Status',
        accessor: 'ProvisioningStatus',
        Cell: ({ value }: { value: number }) => {
          switch (value) {
            case 1:
              return '🟡 Provisioning';
            case 2:
              return '🟢 Ready';
            case 3:
              return '🟠 Not Provisioned';
            case 4:
              return '🔴 Provisioning Failed';
            default:
              return '🟠 Not Provisioned';
          }
        },
        width: 200,
      },
    ],
    []
  );
  const [current_filter, setCurrentFilter] = useState('1');
  const count = (stage: 1 | 2 | 3 | 4): number => {
    console.log(Object.entries(getAllDigitalContractsData))
    return Object.entries(getAllDigitalContractsData).filter(
      ([key, value]) => getDCStage(value.ContractStage, value.ExpirationTime) == stage
    ).length;
  };

  const filters = [
    {
      name: 'Waiting for Approval',
      value: '1',
      count: count(1),
    },
    {
      name: 'Waiting for Activation',
      value: '2',
      count: count(2),
    },
    {
      name: 'Activated',
      value: '3',
      count: count(3),
    },
    {
      name: 'Expired',
      value: '4',
      count: count(4),
    },
  ];

  const parsedData = Object.entries(getAllDigitalContractsData)
    .filter(
      (contract) =>
        getDCStage(
          contract[1].ContractStage,
          contract[1].ExpirationTime
        ).toString() == current_filter
    )
    .map(([key, value]) => {
      return {
        key,
        ...value,
        PartnerOrg: getPartnerOrg(
          userData,
          value.DataOwnerOrganization,
          value.DOOName,
          value.ROName
        ),
      };
    })
    .sort((elem1, elem2) => -(elem1.LastActivity - elem2.LastActivity));

  return (
    <>
      <TableFilter
        current_filter={current_filter}
        setCurrentFilter={setCurrentFilter}
        filters={filters}
      />
      <Margin size={5} />
      <Table
        base_url="/dashboard/digital-contracts"
        id_accessor="key"
        columns={columns}
        data={parsedData}
      />
    </>
  );
};

export default DigitalContractsSuccess;
