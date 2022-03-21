import React from 'react';

import { ConditionalRender } from '@components/ConditionalRender';

import { TReopenAccountProps } from './ReopenAccount.types';

import ReopenAccountForm from './ReopenAccount.form';

import ReopenAccountSuccess from './ReopenAccount.success';
import ReopenAccountFailure from './ReopenAccount.failure';
import { useEffect } from 'react';

const DeleteAccount: React.FC<TReopenAccountProps> = ({
  putAccountManagerState,
  putAccountManagerStart,
  putAccountManagerReset,
  getAllAccountManagersStart,
  getAllAccountManagersReset,
  OrganizationGuid,
  closeModal,
  UserGuid
}) => {
  useEffect(() => {
    putAccountManagerReset();
  }, []);
  return (
    <ConditionalRender
      //@ts-ignore
      state={putAccountManagerState}
      success={() => <ReopenAccountSuccess closeModal={() => {
        closeModal()
        getAllAccountManagersReset();
        getAllAccountManagersStart({OrganizationGuid: OrganizationGuid})
      }}
      />
      }
      failure={ReopenAccountFailure}
    >
      <ReopenAccountForm
        putAccountManagerStart={putAccountManagerStart}
        putAccountManagerReset={putAccountManagerReset}
        UserGuid={UserGuid}
      />
    </ConditionalRender>
  );
};

export default DeleteAccount;
