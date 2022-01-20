import React from 'react';
import Button from '@components/Button';
import { TReopenAccountSuccessProps } from './ReopenAccount.types';

const ReopenAccountSuccess = ({ closeModal }: TReopenAccountSuccessProps) => {
  return (
    <>
      <h1>
        This account has been reopened successfully. Please click continue to
        return to the User Manager.
      </h1>
      <Button onClick={closeModal}>Continue</Button>
    </>
  );
};

export default ReopenAccountSuccess;
