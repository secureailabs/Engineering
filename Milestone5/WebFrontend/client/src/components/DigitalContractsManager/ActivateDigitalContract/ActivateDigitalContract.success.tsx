import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '@components/Button';

const ActivateDigitalContractSuccess = () => {
  const navigate = useNavigate();
  return (
    <>
      <h1>
        The digital contract was successfully activated. Please click continue
        to return to the main menu.
      </h1>
      <Button onClick={() => navigate('/dashboard')}>Continue</Button>
    </>
  );
};

export default ActivateDigitalContractSuccess;
