import React from 'react';
import Button from '@components/Button';
import { TDeleteAccountSuccessProps } from './DeleteAccount.types';

const DeleteAccountSuccess = ({ closeModal }: TDeleteAccountSuccessProps) => {
  return (
    <>
      <h1>
        This account has been closed successfully. Please click continue to
        return to the User Manager.
      </h1>
      <Button onClick={closeModal}>Continue</Button>
    </>
  );
};

export default DeleteAccountSuccess;
