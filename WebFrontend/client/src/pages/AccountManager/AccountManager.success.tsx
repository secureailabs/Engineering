import React, { useState } from 'react';

import { TAccountManagerSuccessProps } from './AccountManager.types';

import GetAllAccounts from '@components/AccountManager/GetAllAccounts';

const AccountManagerSuccess: React.FC<TAccountManagerSuccessProps> = ({
  accountsFilter,
  getAllAccountManagersData,
  setAccountManagerID,
}) => {
  console.log(accountsFilter)
  console.log(getAllAccountManagersData.OrganizationUsers)
  const parsedData = Object.entries(getAllAccountManagersData.OrganizationUsers)
  .map(
    ([key, value]) => {
      return {
        key,
        ...value,
      };
    }
  )
  .filter((elem) => 
    (accountsFilter == 'open' && ( 
      (elem.AccountStatus == 0)
      ||
      (elem.AccountStatus == 1)))
    ||
    (accountsFilter == 'closed' && (
      (elem.AccountStatus == 2)
      ||
      (elem.AccountStatus == 3)
    )))
  .sort((elem1, elem2) => elem1.Email.localeCompare(elem2.Email));

  return <GetAllAccounts data={parsedData} setAccountManagerID={setAccountManagerID}/>;
};

export default AccountManagerSuccess;
