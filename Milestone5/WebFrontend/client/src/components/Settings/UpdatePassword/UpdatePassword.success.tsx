import React from 'react';

import UpdatePasswordForm from './UpdatePassword.form';

import { TUpdatePasswordSuccessProps } from './UpdatePassword.types';

const UpdatePasswordSuccess: React.FC<TUpdatePasswordSuccessProps> = ({
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
        Password updated successfully
      </h2>
      <br />
      <br />
    </>
  );
};

export default UpdatePasswordSuccess;
