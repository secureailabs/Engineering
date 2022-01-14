import React from 'react';

import Button from '@components/Button';
import { useHistory } from 'react-router';

const AcceptDigitalContractSuccess = () => {
  const history = useHistory();
  return (
    <>
      <h1>
        The digital contract was successfully accepted. Please click continue to
        return to the main menu.
      </h1>
      <Button onClick={() => history.push('/dashboard')}>Continue</Button>
    </>
  );
};

export default AcceptDigitalContractSuccess;
