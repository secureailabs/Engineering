import React from 'react';
import { useHistory } from 'react-router-dom';
import Button from '@components/Button';

const ProvisionDigitalContractSuccess = () => {
  const history = useHistory();
  return (
    <>
      <h1>
        The digital contract was successfully provisioned. Please click continue to
        return to the main menu.
      </h1>
      <Button onClick={() => history.push('/dashboard')}>Continue</Button>
    </>
  );
};

export default ProvisionDigitalContractSuccess;
