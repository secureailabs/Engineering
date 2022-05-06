import React from 'react';

import Modal from '@secureailabs/web-ui/components/Modal';
import Button from '@secureailabs/web-ui/components/Button';

import { TRequestDataAccessFormFailureProps } from './RequestDataAccessForm.types';

const RequestDatasetAccessFormFailure: React.FC<TRequestDataAccessFormFailureProps> = ({ setIsOpen, error }) => {
  return (
    <Modal
      title='Request Dataset Access'
      description="An error has occured, please try again later."
      close={() => setIsOpen(false)}
    >
      <Button button_type='primary' full onClick={() => setIsOpen(false)}>Back</Button>
    </Modal>
  )
};

export default RequestDatasetAccessFormFailure;
