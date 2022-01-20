import React from 'react';

import UpdateUserForm from './UpdateUser.form';

import { TUpdateUserSuccessProps } from './UpdateUser.types';

const UpdateUserSuccess: React.FC<TUpdateUserSuccessProps> = ({
  userData,
  putUpdateUserReset,
  putUpdateUserStart,
}) => {
  return (
    <>
      <UpdateUserForm
        userData={userData}
        putUpdateUserReset={putUpdateUserReset}
        putUpdateUserStart={putUpdateUserStart}
      />
      <h2
        style={{
          textAlign: 'center',
          paddingTop: '0',
          paddingBottom: '4rem',
        }}
      >
        User details updated successfully. Please relogin to view the updated
        information
      </h2>
      <br />
      <br />
    </>
  );
};

export default UpdateUserSuccess;
