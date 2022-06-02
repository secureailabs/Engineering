import React from 'react';

import { TUserManagerList } from './UserManagerList.types';
import { useTable, useSortBy, useFlexLayout } from 'react-table';

const DatasetList: React.FC<TUserManagerList> = () => {
// = ({ Datasets, setDatasetID }) 

  // console.log(Datasets);

  const columns = React.useMemo(
    () => [
      {
        Header: 'Name',
        accessor: 'DatasetName',
        width: 150,
      },
      {
        Header: 'Publish Date',
        accessor: 'PublishDate',
        width: 50,
      },
      {
        Header: 'Keywords',
        accessor: 'Keywords',
        width: 300,
      },
      {
        Header: 'Dataset Owner',
        accessor: 'OrganizationName',
        width: 150,
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
      data: Datasets,
    },
    useSortBy,
    useFlexLayout
  );

  return (
    <></>
    // <table {...getTableProps()}>
    //   <thead>
    //     {headerGroups.map((headerGroup) => (
    //       <tr {...headerGroup.getHeaderGroupProps()}>
    //         {headerGroup.headers.map((column) => (
    //           // Add the sorting props to control sorting. For this example
    //           // we can add them into the header props
    //           //@ts-ignore
    //           <th {...column.getHeaderProps(column.getSortByToggleProps())}>
    //             {column.render('Header')}
    //             {/* Add a sort direction indicator */}
    //             <span>
    //               {
    //                 //@ts-ignore
    //                 column.isSorted ? (column.isSortedDesc ? ' 🔽' : ' 🔼') : ''
    //               }
    //             </span>
    //           </th>
    //         ))}
    //       </tr>
    //     ))}
    //   </thead>
    //   <tbody {...getTableBodyProps()}>
    //     {rows.map((row, i) => {
    //       prepareRow(row);
    //       return (
    //         <tr {...row.getRowProps()}>
    //           {row.cells.map((cell) => {
    //             return (
    //               <td
    //                 {...cell.getCellProps()}
    //                 onClick={() => {
    //                   //@ts-ignore
    //                   setDatasetID(cell.row.original.key);
    //                 }}
    //               >
    //                 {cell.render('Cell')}
    //               </td>
    //             );
    //           })}
    //         </tr>
    //       );
    //     })}
    //   </tbody>
    // </table>
  );
};

export default DatasetList;
