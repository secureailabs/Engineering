import React, { useEffect } from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TRegisterAccountProps } from './RegisterAccount.types';

import RegisterAccountForm from './RegisterAccount.form';
import RegisterAccountSuccess from './RegisterAccount.success';
import RegisterAccountFailure from './RegisterAccount.failure';

const RegisterAccount: React.FC<TRegisterAccountProps> = ({
  postAccountManagerStart,
  postAccountManagerReset,
  postAccountManagerState,
  getAllAccountManagersReset,
  getAllAccountManagersStart,
  userData,
  closeModal
}) => {
  useEffect(() => {
    postAccountManagerReset();
  }, []);
  return (
    <ConditionalRender
      //@ts-ignore
      state={
        postAccountManagerState
        // null
      }
      success={() => (
        <RegisterAccountSuccess
          closeModal={() => {
            closeModal();
            getAllAccountManagersReset();
            getAllAccountManagersStart(userData?.OrganizationGuid || '');
          }}
        />
      )}
      failure={() => <RegisterAccountFailure />}
    >
      <RegisterAccountForm
        postAccountManagerStart={postAccountManagerStart}
        postAccountManagerReset={postAccountManagerReset}
        userData={userData}
      />
    </ConditionalRender>
  );
};

export default RegisterAccount;
