import React from 'react';

import Modal from '@secureailabs/web-ui/components/Modal';
import Button from '@secureailabs/web-ui/components/Button';

import { TActivateDigitalContractFormFailureProps } from './ActivateDigitalContractForm.types';

const ActivateDigitalContractFormFailure: React.FC<TActivateDigitalContractFormFailureProps> = ({ setIsOpen, error }) => {
  return (
    <Modal
      title='Activate Digital Contract'
      description="An error has occured, please try again later."
      close={() => setIsOpen(false)}
    >
      <Button button_type='primary' full onClick={() => setIsOpen(false)}>Back</Button>
    </Modal>
  )
};

export default ActivateDigitalContractFormFailure;
