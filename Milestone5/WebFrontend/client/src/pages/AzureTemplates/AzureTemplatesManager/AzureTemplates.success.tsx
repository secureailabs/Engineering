import React from 'react';

import { TAzureTemplatesSuccessProps } from './AzureTemplates.types';

import Table from '@components/Table';
const AccountManagerSuccess: React.FC<TAzureTemplatesSuccessProps> = ({
  getAllAzureTemplatesData,
}) => {
  const parsedData = Object.entries(getAllAzureTemplatesData.Templates)
    .map(([key, value]) => {
      return {
        TemplateGuid: key,
        ...value,
      };
    })
    .sort((elem1, elem2) => elem1.Name.localeCompare(elem2.Name));

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

  return (
    <Table
      base_url="/dashboard/azure-templates"
      id_accessor="TemplateGuid"
      columns={columns}
      data={parsedData}
    />
  );
};

export default AccountManagerSuccess;
