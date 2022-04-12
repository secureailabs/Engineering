import React from 'react';
import { useTable, useSortBy, useFlexLayout } from 'react-table';
import { TGetAllAccounts } from './GetAllAccounts.types'
import accessRightsNumberToString from '@utils/accessRightsNumberToString';

const GetAllAccounts: React.FC<TGetAllAccounts> = ({
  setAccountManagerID,
  data
}) => {
  const columns = React.useMemo(
    () => [
      {
        Header: 'Email',
        accessor: 'Email',
        width: 200,
      },
      {
        Header: 'Name',
        accessor: 'Username',
        width: 200,
      },
      {
        Header: 'Job Title',
        accessor: 'Title',
        width: 200,
      },
      {
        Header: 'Phone Number',
        accessor: 'PhoneNumber',
        width: 200,
      },
      {
        Header: 'Access Rights',
        accessor: 'AccessRights',
        Cell: ({value}: {value: 1 | 2 | 3 | 4 | 5 | 6}) => accessRightsNumberToString(value),
        width: 200
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
      autoResetSortBy:false,
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
                return (
                  <td
                    {...cell.getCellProps()}
                    onClick={() => {
                      setAccountManagerID(cell.row.original.UserGuid);
                      window.scrollTo(0, 0);
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

export default GetAllAccounts;
