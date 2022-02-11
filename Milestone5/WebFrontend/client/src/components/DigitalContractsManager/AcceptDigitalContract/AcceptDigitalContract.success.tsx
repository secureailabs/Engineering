import React from 'react';

import Button from '@components/Button';
import { useNavigate } from 'react-router';

const AcceptDigitalContractSuccess = () => {
  const navigate = useNavigate();
  return (
    <>
      <h1>
        The digital contract was successfully accepted. Please click continue to
        return to the main menu.
      </h1>
      <Button onClick={() => navigate('/dashboard')}>Continue</Button>
    </>
  );
};

export default AcceptDigitalContractSuccess;
