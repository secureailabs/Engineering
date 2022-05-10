import React from 'react';

import Modal from '@secureailabs/web-ui/components/Modal';
import Button from '@secureailabs/web-ui/components/Button';

import { TAcceptDigitalContractFormSuccessProps } from './AcceptDigitalContractForm.types';

const RequestDatasetAccessFormSuccess: React.FC<TAcceptDigitalContractFormSuccessProps> = ({ UrlOnSuccess }) => {
  return (
    <Modal
      title='Accept Digital Contract'
      description="You accepted this digital contract successfully."
      close={() =>  window.location.href = UrlOnSuccess}
    >
      <Button button_type='primary' full onClick={() => window.location.href = UrlOnSuccess}>Go back to digital contract list</Button>
    </Modal>
  )
};

export default RequestDatasetAccessFormSuccess;
