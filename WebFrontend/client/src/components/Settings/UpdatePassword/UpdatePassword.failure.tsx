import React from 'react';

import UpdatePasswordForm from './UpdatePassword.form';
import { TUpdatePasswordFailureProps } from './UpdatePassword.types';

const UpdatePasswordFailure: React.FC<TUpdatePasswordFailureProps> = ({
  userData,
  putUpdatePasswordReset,
  putUpdatePasswordStart,
}) => {
  return (
    <>
      <UpdatePasswordForm
        userData={userData}
        putUpdatePasswordReset={putUpdatePasswordReset}
        putUpdatePasswordStart={putUpdatePasswordStart}
      />
      <h2
        style={{
          textAlign: 'center',
          paddingTop: '0',
          paddingBottom: '4rem',
        }}
      >
        There was an error updating your password
      </h2>
      <br />
      <br />
    </>
  );
};

export default UpdatePasswordFailure;
