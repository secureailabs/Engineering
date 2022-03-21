import React from 'react';
import { useTable, useSortBy, useFlexLayout } from 'react-table';
import { TAzureTemplatesList } from './AzureTemplatesList.types';

const AzureTemplatesList: React.FC<TAzureTemplatesList> = ({
  setAzureTemplateID,
  data,
  onClick,
}) => {
  const columns = React.useMemo(
    () => [
      {
        Header: 'Name',
        accessor: 'Name',
        width: 200,
      },
      {
        Header: 'Template Region',
        accessor: 'HostRegion',
        width: 200,
      },
      {
        Header: 'Subscription ID',
        accessor: 'SubscriptionID',
        width: 200,
      },
      {
        Header: 'Azure Template State',
        accessor: 'State',
        width: 200,
        Cell: ({ value }: { value: number }) => {
          switch (value) {
            case 1:
              return '🟡 Initializing';
            case 2:
              return '🟡 Creating Virtual Network';
            case 3:
              return '🟡 Creating Network Security Group';
            case 4:
              return '🔴 Failed Creating Virtual Network';
            case 5:
              return '🔴 Failed Creating Network Security Group';
            case 6:
              return '🟢 Ready';
            case 7:
              return '🔴 Image Does Not Exist';
            case 8:
              return '🔴 Invalid Credentials';
            case 9:
              return '🟡 Creating Image';
            case 10:
              return '🔴 Failed Creating Image';
            case 11:
              return '🔴 Server Error';
          }
        },
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
      //@ts-ignore
      data,
      //@ts-ignore
      autoResetSortBy: false,
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
                      if (onClick) {
                        onClick(cell.row.original.TemplateGuid);
                      } else {
                        setAzureTemplateID(cell.row.original.TemplateGuid);
                        window.scrollTo(0, 0);
                      }
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

export default AzureTemplatesList;
