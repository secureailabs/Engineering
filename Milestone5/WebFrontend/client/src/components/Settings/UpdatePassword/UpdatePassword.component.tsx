import React, { useEffect } from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TUpdatePasswordProps } from './UpdatePassword.types';

import UpdatePasswordForm from './UpdatePassword.form';
import UpdatePasswordSuccess from './UpdatePassword.success';
import UpdatePasswordFailure from './UpdatePassword.failure';

const UpdatePassword: React.FC<TUpdatePasswordProps> = ({
  putUpdatePasswordReset,
  putUpdatePasswordStart,
  putUpdatePasswordState,
  userData,
}) => {
  useEffect(() => {
    putUpdatePasswordReset();
  }, []);
  return (
    <ConditionalRender
      //@ts-ignore
      state={putUpdatePasswordState}
      success={() => (
        <UpdatePasswordSuccess
          userData={userData}
          putUpdatePasswordReset={putUpdatePasswordReset}
          putUpdatePasswordStart={putUpdatePasswordStart}
        />
      )}
      failure={() => (
        <UpdatePasswordFailure
          userData={userData}
          putUpdatePasswordReset={putUpdatePasswordReset}
          putUpdatePasswordStart={putUpdatePasswordStart}
        />
      )}
    >
      <UpdatePasswordForm
        userData={userData}
        putUpdatePasswordReset={putUpdatePasswordReset}
        putUpdatePasswordStart={putUpdatePasswordStart}
      />
    </ConditionalRender>
  );
};

export default UpdatePassword;
