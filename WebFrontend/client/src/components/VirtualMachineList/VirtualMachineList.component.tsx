import React from 'react';

import { TVirtualMachineList } from './VirtualMachineList.types';
import { useTable, useSortBy, useFlexLayout } from 'react-table';

const VirtualMachineList: React.FC<TVirtualMachineList> = ({
  setVirtualMachineID,
  data,
}) => {
  const initialState = {
    sortBy: [
      {
          id: 'State',
          desc: false
      }
  ]
  }
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
              return '🟢 Ready for Computation'
            case 6:
              return '🟢 In Use'
            case 7:
              return '🟠 Shutting Down'
            case 8:
              return '🔴 Deleted'
            case 9:
              return '🟠 Deletion Failed';
            case 10:
              return '🔴 Creation Failed';
            }
        },
        width: 200,
      },
    ],
    []
  );
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable(
    {
      //@ts-ignore
      columns,
      data,
      autoResetSortBy: false,
      // @ts-ignore
      initialState: initialState
    },
    useSortBy,
    // useFlexLayout
  );

  return (
    <table {...getTableProps()}>
      <thead>
        {headerGroups.map((headerGroup) => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map((column) => (
              // Add the sorting props to control sorting. For this example
              // we can add them into the header props
              //@ts-ignore
              <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                {column.render('Header')}
                {/* Add a sort direction indicator */}
                <span>
                  {
                    //@ts-ignore
                    column.isSorted ? (column.isSortedDesc ? ' 🔽' : ' 🔼') : ''
                  }
                </span>
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody {...getTableBodyProps()}>
        {rows.map((row, i) => {
          prepareRow(row);
          return (
            <tr {...row.getRowProps()}>
              {row.cells.map((cell) => {
                console.log('CELL: ', cell);

                return (
                  <td
                    {...cell.getCellProps()}
                    onClick={() => {
                      window.scrollTo({top: 0})
                      //@ts-ignore
                      setVirtualMachineID(cell.row.original.VirtualMachineGuid);
                    }}
                  >
                    {cell.render('Cell')}
                  </td>
                );
              })}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

export default VirtualMachineList;
