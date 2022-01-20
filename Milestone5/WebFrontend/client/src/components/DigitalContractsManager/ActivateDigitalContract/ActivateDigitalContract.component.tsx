import React from 'react';

import { ConditionalRender } from '@components/ConditionalRender';

import { TActivateDigitalContractProps } from './ActivateDigitalContract.types';

import ActivateDigitalContractForm from './ActivateDigitalContract.form';

import ActivateDigitalContractSuccess from './ActivateDigitalContract.success';
import ActivateDigitalContractFailure from './ActivateDigitalContract.failure';
import { useEffect } from 'react';

const ActivateDigitalContract: React.FC<TActivateDigitalContractProps> = ({
  patchActivateDigitalContractState,
  patchActivateDigitalContractStart,
  patchActivateDigitalContractReset,
  getDigitalContractData,
  DigitalContractGuid,
}) => {
  useEffect(() => {
    patchActivateDigitalContractReset();
  }, []);
  return (
    <ConditionalRender
      //@ts-ignore
      state={patchActivateDigitalContractState}
      success={ActivateDigitalContractSuccess}
      failure={ActivateDigitalContractFailure}
    >
      <ActivateDigitalContractForm
        patchActivateDigitalContractStart={patchActivateDigitalContractStart}
        patchActivateDigitalContractReset={patchActivateDigitalContractReset}
        getDigitalContractData={getDigitalContractData}
        DigitalContractGuid={DigitalContractGuid}
      />
    </ConditionalRender>
  );
};

export default ActivateDigitalContract;
