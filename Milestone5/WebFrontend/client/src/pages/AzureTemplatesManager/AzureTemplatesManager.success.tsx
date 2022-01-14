import React, { useState } from 'react';

import { TAzureTemplatesManagerSuccessProps } from './AzureTemplatesManager.types';

import AzureTemplatesList from '@components/AzureTemplatesManager/AzureTemplatesList';

const AccountManagerSuccess: React.FC<TAzureTemplatesManagerSuccessProps> = ({
  listAzureTemplatesData,
  setAzureTemplateID,
}) => {
 
  const parsedData = Object.entries(listAzureTemplatesData.Templates)
  .map(
    ([key, value]) => {
      return {
        TemplateGuid: key,
        ...value,
      };
    }
  )
  .sort((elem1, elem2) => elem1.Name.localeCompare(elem2.Name));

  return <AzureTemplatesList data={parsedData} setAzureTemplateID={setAzureTemplateID}/>;
};

export default AccountManagerSuccess;
