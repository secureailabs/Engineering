import React from 'react';

import { ConditionalRender } from '@components/ConditionalRender';

import { TDeleteAccountProps } from './DeleteAccount.types';

import DeleteAccountForm from './DeleteAccount.form';

import DeleteAccountSuccess from './DeleteAccount.success';
import DeleteAccountFailure from './DeleteAccount.failure';
import { useEffect } from 'react';

const DeleteAccount: React.FC<TDeleteAccountProps> = ({
  deleteAccountManagerState,
  deleteAccountManagerStart,
  deleteAccountManagerReset,
  getAllAccountManagersStart,
  getAllAccountManagersReset,
  closeModal,
  OrganizationGuid,
  UserGuid,
}) => {
  useEffect(() => {
    deleteAccountManagerReset();
  }, []);
  return (
    <ConditionalRender
      //@ts-ignore
      state={deleteAccountManagerState}
      success={() => 
        <DeleteAccountSuccess 
          closeModal={() => {
            closeModal()
            getAllAccountManagersReset()
            getAllAccountManagersStart({OrganizationGuid: OrganizationGuid})
          }}
        />
      }
      failure={DeleteAccountFailure}
    >
      <DeleteAccountForm
        deleteAccountManagerStart={deleteAccountManagerStart}
        deleteAccountManagerReset={deleteAccountManagerReset}
        UserGuid={UserGuid}
      />
    </ConditionalRender>
  );
};

export default DeleteAccount;
