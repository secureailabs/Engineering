import React from 'react';

import Button from '@components/Button';

import type { TRegisterAzureTemplateSuccess } from './RegisterAzureTemplate.types';

const RegisterAzureTemplateSuccess: React.FC<TRegisterAzureTemplateSuccess> = ({
  closeModal,
}) => {
  return (
    <>
      <h1>
        The Azure Template was created successfully. Please click continue to return to
        the Azure Template Manager.
      </h1>
      <Button onClick={closeModal}>Continue</Button>
    </>
  );
};

export default RegisterAzureTemplateSuccess;
