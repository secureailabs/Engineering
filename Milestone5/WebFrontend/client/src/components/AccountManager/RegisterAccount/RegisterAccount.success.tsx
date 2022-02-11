import React from 'react';

import Button from '@components/Button';

import type { TRegisterAccountSuccess } from './RegisterAccount.types';

const RegisterAccountSuccess: React.FC<TRegisterAccountSuccess> = ({
  closeModal,
}) => {
  return (
    <>
      <h1>
        The user was created successfully. Please click continue to return to
        the Account Manager.
      </h1>
      <Button onClick={closeModal}>Continue</Button>
    </>
  );
};

export default RegisterAccountSuccess;
