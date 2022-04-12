import React from 'react';

import Button from '@components/Button';

import { useHistory } from 'react-router-dom';

import type { TRegisterDigitalContractSuccess } from './RegisterDigitalContract.types';

const RegisterDigitalContractSuccess: React.FC<TRegisterDigitalContractSuccess> = ({
  closeModal,
}) => {
  const history = useHistory();
  return (
    <>
      <h1>
        The access request was sent successfully. Please click continue to
        return to the main menu.
      </h1>
      <Button onClick={() => history.push('/dashboard')}>Continue</Button>
    </>
  );
};

export default RegisterDigitalContractSuccess;
