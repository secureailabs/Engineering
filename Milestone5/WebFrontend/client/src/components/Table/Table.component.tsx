import React from 'react';
import { useTable, useSortBy, useFlexLayout } from 'react-table';
import Text from '@secureailabs/web-ui/components/Text';
import type TTable from './Table.types';
import { useNavigate } from 'react-router-dom';

const Table: React.FC<TTable> = ({
  data,
  initial_state,
  columns,
  id_accessor,
  base_url,
}) => {
  const navigate = useNavigate();
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable(
    {
      columns,
      data,
      initialState: initial_state,
    },
    useSortBy
  );

  return (
    <table className="table" {...getTableProps()}>
      <thead>
        {headerGroups.map((headerGroup) => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map((column) => (
              // Add the sorting props to control sorting. For this example
              // we can add them into the header props
              // @ts-ignore
              <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                <Text fontSize="14px" fontWeight={600}>
                  {column.render('Header')}
                </Text>
                {/* Add a sort direction indicator */}
                <span>
                  {
                    // @ts-ignore
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
            <tr
              {...row.getRowProps()}
              onClick={() => {
                navigate(`${base_url}/${row.original[id_accessor]}`);
              }}
            >
              {row.cells.map((cell) => {
                return (
                  <td {...cell.getCellProps()} onClick={() => {}}>
                    <Text fontSize="12px" fontWeight={500}>
                      {cell.render('Cell')}
                    </Text>
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

export default Table;
