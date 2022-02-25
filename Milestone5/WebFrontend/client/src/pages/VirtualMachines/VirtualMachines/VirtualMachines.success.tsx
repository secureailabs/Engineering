import React, { useState } from 'react';

import Table from '@components/Table';

import { TVirtualMachinesSuccessProps } from './VirtualMachines.types';

import { TGetVirtualMachineSuccess } from '@redux/virtualMachineManager/virtualMachineManager.typeDefs';

import TableFilter from '@secureailabs/web-ui/components/TableFilter';

import Margin from '@secureailabs/web-ui/components/Margin';

const VirtualMachineSuccess: React.FC<TVirtualMachinesSuccessProps> = ({
  getAllVirtualMachinesData,
}) => {
  const columns = React.useMemo(
    () => [
      {
        Header: 'IP Address',
        accessor: 'IPAddress',
        width: 200,
      },
      {
        Header: 'Region',
        accessor: 'HostRegion',
        width: 100,
      },
      {
        Header: 'CPUs',
        accessor: 'NumberOfVCPU',
        width: 50,
      },
      {
        Header: 'Start Time',
        accessor: 'StartTime',
        Cell: ({ value }: { value: number }) =>
          new Date(value * 1000).toLocaleDateString('en-US', {
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
        Header: 'Data Owner',
        accessor: 'DigitalContract.DOOName',

        width: 200,
      },
      {
        Header: 'Digital Contract',
        accessor: 'DigitalContractTitle',
        width: 400,
      },
      {
        Header: 'State',
        accessor: 'State',
        Cell: ({ value }: { value: number }) => {
          console.log('VALUE: ', value);
          switch (value) {
            case 1:
              return '🟡 Starting';
            case 2:
              return '🟡 Configuring';
            case 3:
              return '🟡 Initializing';
            case 4:
              return '🟡 Waiting for Data';
            case 5:
              return '🟢 Ready for Computation';
            case 6:
              return '🟢 In Use';
            case 7:
              return '🟠 Shutting Down';
            case 8:
              return '🔴 Deleted';
            case 9:
              return '🟠 Deletion Failed';
            case 10:
              return '🔴 Creation Failed';
          }
          return 'Error';
        },
        width: 200,
      },
    ],
    []
  );

  const [current_filter, setCurrentFilter] = useState('Researcher');
  const vmCount = (host: 'Researcher' | 'Data Owner') => {
    let count = 0;
    Object.keys(getAllVirtualMachinesData).map((el) => {
      if (getAllVirtualMachinesData[el].HostForVirtualMachines == host) {
        count += Object.keys(
          getAllVirtualMachinesData[el].VirtualMachinesAssociatedWithDc
        ).length;
      }
    });
    return count;
  };

  const filters = [
    {
      name: 'Researcher',
      value: 'Researcher',
      count: vmCount('Researcher'),
    },
    {
      name: 'Data Owner',
      value: 'Data Owner',
      count: vmCount('Data Owner'),
    },
  ];

  const parsedData: TGetVirtualMachineSuccess[] = [];
  Object.entries(getAllVirtualMachinesData)
    .filter((virtualMachines) => {
      if (virtualMachines[1].HostForVirtualMachines === current_filter) {
        return true;
      }
    })
    .forEach(([key, value]) => {
      // console.log(value.VirtualMachinesAssociatedWithDc)
      Object.entries(value.VirtualMachinesAssociatedWithDc).forEach(
        ([key, value]) => {
          parsedData.push({
            ...value,
          });
        }
      );
    });

  return (
    <>
      <TableFilter
        current_filter={current_filter}
        setCurrentFilter={setCurrentFilter}
        filters={filters}
      />
      <Margin size={5} />
      <Table
        base_url="/dashboard/virtual-machines"
        id_accessor="VirtualMachineGuid"
        columns={columns}
        data={parsedData}
      />
    </>
  );
};

export default VirtualMachineSuccess;
