import React from 'react';

import { ConditionalRender } from '@components/ConditionalRender';

import { TAcceptDigitalContractProps } from './AcceptDigitalContract.types';

import AcceptDigitalContractForm from './AcceptDigitalContract.form';

import AcceptDigitalContractSuccess from './AcceptDigitalContract.success';
import AcceptDigitalContractFailure from './AcceptDigitalContract.failure';
import { useEffect } from 'react';

const AcceptDigitalContract: React.FC<TAcceptDigitalContractProps> = ({
  patchAcceptDigitalContractState,
  patchAcceptDigitalContractStart,
  patchAcceptDigitalContractReset,
  DigitalContractGuid,
}) => {
  useEffect(() => {
    patchAcceptDigitalContractReset();
  }, []);
  return (
    <ConditionalRender
      //@ts-ignore
      state={patchAcceptDigitalContractState}
      success={AcceptDigitalContractSuccess}
      failure={AcceptDigitalContractFailure}
    >
      <AcceptDigitalContractForm
        patchAcceptDigitalContractStart={patchAcceptDigitalContractStart}
        patchAcceptDigitalContractReset={patchAcceptDigitalContractReset}
        DigitalContractGuid={DigitalContractGuid}
      />
    </ConditionalRender>
  );
};

export default AcceptDigitalContract;
