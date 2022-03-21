import React from 'react';

import getDCStage from '@utils/getDCStage';
import { TDigitalContractList } from './DigitalContractList.types';
import { useTable, useSortBy, useFlexLayout } from 'react-table';

const DigitalContractList: React.FC<TDigitalContractList> = ({
  setDigitalContractID,
  data,
  stage
}) => { 
  let columns = React.useMemo(
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
        Header: 'Provisioning Status',
        accessor: 'ProvisioningStatus',
        Cell: ({ value }: { value: number }) => {
          switch (value) {
            case 1:
              return '🟡 Provisioning';
              break;
            case 2:
              return '🟢 Ready';
              break;
            case 3:
              return '🟠 Not Provisioned';
              break;
            case 4:
              return '🔴 Provisioning Failed';
            default:
              return '🟠 Not Provisioned';
              break;
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
    },
    useSortBy,
    // useFlexLayout
  );

  return (
    <div className='mainlisttable'>
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
                if (cell.column.Header === 'Provisioning Status') {
                  console.log(cell.value);
                  let color;
                  switch (cell.value) {
                    case 1:
                      color = 'yellow';
                      break;
                    case 2:
                      color = 'green';
                      break;
                    case 3:
                      color = 'grey';
                      break;
                    case 4:
                      color = 'red';
                    default:
                      color = 'grey';
                      break;
                  }
                  return (
                    <td
                      {...cell.getCellProps()}
                      onClick={() => {
                        //@ts-ignore
                        setDigitalContractID(cell.row.original.key);
                      }}
                    >
                      <p
                        style={{
                          // color,
                          padding: 0,
                          margin: 0,
                        }}
                      >
                        {cell.render('Cell')}
                      </p>
                    </td>
                  );
                }
                return (
                  <td
                    {...cell.getCellProps()}
                    onClick={() => {
                      //@ts-ignore
                      setDigitalContractID(cell.row.original.key);
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
    </div>
  );
};

export default DigitalContractList;
