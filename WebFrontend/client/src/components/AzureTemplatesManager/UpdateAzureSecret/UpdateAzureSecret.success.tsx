import React from 'react';

import Button from '@components/Button';
import { useHistory } from 'react-router';
import { TUpdateAzureSecretSuccessProps } from './UpdateAzureSecret.types';

const UpdateAzureSecretSuccess = ({
  closeModal
}: TUpdateAzureSecretSuccessProps) => {
  return (
    <>
      <h1>
        The Azure Secret was successfully updated. Please click continue to
        return to the template settings.
      </h1>
      <Button onClick={() => closeModal()}>Continue</Button>
    </>
  )
};

export default UpdateAzureSecretSuccess;
