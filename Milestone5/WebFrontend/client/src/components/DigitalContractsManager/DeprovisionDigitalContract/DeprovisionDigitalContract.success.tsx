import React from 'react';
import { useHistory } from 'react-router-dom';
import Button from '@components/Button';

const DeprovisionDigitalContractSuccess = () => {
  const history = useHistory();
  return (
    <>
      <h1>
        The digital contract was successfully deprovisioned. Please click continue to
        return to the main menu.
      </h1>
      <Button onClick={() => history.push('/dashboard')}>Continue</Button>
    </>
  );
};

export default DeprovisionDigitalContractSuccess;
