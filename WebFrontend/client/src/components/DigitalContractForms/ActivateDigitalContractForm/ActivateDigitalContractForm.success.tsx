import React from 'react';

import Modal from '@secureailabs/web-ui/components/Modal';
import Button from '@secureailabs/web-ui/components/Button';

import { TActivateDigitalContractFormSuccessProps } from './ActivateDigitalContractForm.types';

const ActivateDigitalContractFormSuccess: React.FC<TActivateDigitalContractFormSuccessProps> = ({ UrlOnSuccess }) => {
  return (
    <Modal
      title='Activate Digital Contract'
      description="You activated this digital contract successfully."
      close={() =>  window.location.href = UrlOnSuccess}
    >
      <Button button_type='primary' full onClick={() => window.location.href = UrlOnSuccess}>Go back to digital contract list</Button>
    </Modal>
  )
};

export default ActivateDigitalContractFormSuccess;
