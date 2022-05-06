import React from 'react';

import Modal from '@secureailabs/web-ui/components/Modal';
import Button from '@secureailabs/web-ui/components/Button';

import { TRequestDataAccessFormSuccessProps } from './RequestDataAccessForm.types';

const RequestDatasetAccessFormSuccess: React.FC<TRequestDataAccessFormSuccessProps> = ({ UrlOnSuccess }) => {
  return (
    <Modal
      title='Request Dataset Access'
      description="Your request to access this dataset has been sent successfully."
      close={() =>  window.location.href = UrlOnSuccess}
    >
      <Button button_type='primary' full onClick={() => window.location.href = UrlOnSuccess}>Go back to dataset list</Button>
    </Modal>
  )
};

export default RequestDatasetAccessFormSuccess;
