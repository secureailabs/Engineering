import React, { useState } from 'react';

import { TAzureTemplatesManagerSuccessProps } from './SelectAzureTemplate.types';

import AzureTemplatesList from '@components/AzureTemplatesManager/AzureTemplatesList';

const AccountManagerSuccess: React.FC<TAzureTemplatesManagerSuccessProps> = ({
  listAzureTemplatesData,
  setAzureTemplateID,
  onClick,
}) => {
  const parsedData = Object.entries(listAzureTemplatesData.Templates)
    .map(([key, value]) => {
      return {
        TemplateGuid: key,
        ...value,
      };
    })
    .sort((elem1, elem2) => elem1.Name.localeCompare(elem2.Name));

  return (
    <div className="getallaccounts">
      <AzureTemplatesList
        onClick={onClick}
        data={parsedData}
        setAzureTemplateID={setAzureTemplateID}
      />
    </div>
  );
};

export default AccountManagerSuccess;
