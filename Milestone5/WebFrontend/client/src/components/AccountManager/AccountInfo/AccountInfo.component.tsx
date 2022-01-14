import React from 'react';
// import { ConditionalRender } from '@components/ConditionalRender';

import { TAccountInfo } from './AccountInfo.types';

import AccountInfoSuccess from './AccountInfo.success';
// import AccountInfoFailure from './AccountInfo.failure';
// import { useEffect } from 'react';

const AccountInfo: React.FC<TAccountInfo> = ({
  // getAccountManagerReset,
  // getAccountManagerStart,
  // getAccountManagerState,
  getAccountManagerData,
  accountManagerID,
  slideToPrev,
  userData
}) => {
  // useEffect(() => {
  //   getAccountManagerReset();
  //   getAccountManagerStart(accountManagerID);
  // }, []);
  return (
    // <ConditionalRender
    //   //@ts-ignore
    //   state={getAccountManagerState}
    //   success={() => (
    //     <AccountInfoSuccess
    //       getAccountManagerData={getAccountManagerData}
    //       accountManagerID={accountManagerID}
    //       userData={userData}
    //     />
    //   )}
    //   failure={AccountInfoFailure}
    // >
    //   <></>
    // </ConditionalRender>
    <AccountInfoSuccess
      getAccountManagerData={getAccountManagerData}
      accountManagerID={accountManagerID}
      slideToPrev={slideToPrev}
      userData={userData}
    />
  );
};

export default AccountInfo;
