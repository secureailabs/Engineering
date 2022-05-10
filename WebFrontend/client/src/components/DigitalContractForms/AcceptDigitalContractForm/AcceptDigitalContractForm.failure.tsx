import React from 'react';

import Modal from '@secureailabs/web-ui/components/Modal';
import Button from '@secureailabs/web-ui/components/Button';

import { TAcceptDigitalContractFormFailureProps } from './AcceptDigitalContractForm.types';

const AcceptDigitalContractFormFailure: React.FC<TAcceptDigitalContractFormFailureProps> = ({ setIsOpen, error }) => {
  return (
    <Modal
      title='Accept Digital Contract'
      description="An error has occured, please try again later."
      close={() => setIsOpen(false)}
    >
      <Button button_type='primary' full onClick={() => setIsOpen(false)}>Back</Button>
    </Modal>
  )
};

export default AcceptDigitalContractFormFailure;
