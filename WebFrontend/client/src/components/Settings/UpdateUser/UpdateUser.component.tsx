import React, { useEffect } from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TUpdateUserProps } from './UpdateUser.types';

import UpdateUserForm from './UpdateUser.form';
import UpdateUserSuccess from './UpdateUser.success';
import UpdateUserFailure from './UpdateUser.failure';

const UpdateUser: React.FC<TUpdateUserProps> = ({
  putUpdateUserReset,
  putUpdateUserStart,
  putUpdateUserState,
  userData,
}) => {
  useEffect(() => {
    putUpdateUserReset();
  }, []);
  return (
    <ConditionalRender
      //@ts-ignore
      state={putUpdateUserState}
      success={() => (
        <UpdateUserSuccess
          userData={userData}
          putUpdateUserReset={putUpdateUserReset}
          putUpdateUserStart={putUpdateUserStart}
        />
      )}
      failure={() => (
        <UpdateUserFailure
          userData={userData}
          putUpdateUserReset={putUpdateUserReset}
          putUpdateUserStart={putUpdateUserStart}
        />
      )}
    >
      <UpdateUserForm
        userData={userData}
        putUpdateUserReset={putUpdateUserReset}
        putUpdateUserStart={putUpdateUserStart}
      />
    </ConditionalRender>
  );
};

export default UpdateUser;
