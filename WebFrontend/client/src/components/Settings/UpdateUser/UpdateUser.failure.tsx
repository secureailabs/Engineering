import React from 'react';

import UpdateUserForm from './UpdateUser.form';
import { TUpdateUserFailureProps } from './UpdateUser.types';

const UpdateUserFailure: React.FC<TUpdateUserFailureProps> = ({
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
        There was an error updating your user details
      </h2>
      <br />
      <br />
    </>
  );
};

export default UpdateUserFailure;
