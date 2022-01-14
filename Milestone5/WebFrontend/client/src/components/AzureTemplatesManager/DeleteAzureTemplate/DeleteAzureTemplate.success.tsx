import React from 'react';
import Button from '@components/Button';
import { TDeleteAzureTemplateSuccessProps } from './DeleteAzureTemplate.types'

const DeleteAzureTemplateSuccess = ({ closeModal }: TDeleteAzureTemplateSuccessProps)  => {
  return (
    <>
      <h1>
        This template has been deleted successfully. Please click continue to
        return to the Azure Templates Manager.
      </h1>
      <Button onClick={closeModal}>Continue</Button>
    </>
  );
};

export default DeleteAzureTemplateSuccess;
