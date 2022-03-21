import React from 'react';

import { ConditionalRender } from '@components/ConditionalRender';

import { TProvisionDigitalContractProps } from './ProvisionDigitalContract.types';

import ProvisionDigitalContractForm from './ProvisionDigitalContract.form';

import ProvisionDigitalContractSuccess from './ProvisionDigitalContract.success';
import ProvisionDigitalContractFailure from './ProvisionDigitalContract.failure';
import { useEffect } from 'react';

const ActivateDigitalContract: React.FC<TProvisionDigitalContractProps> = ({
  provisionDigitalContractState,
  provisionDigitalContractStart,
  provisionDigitalContractReset,
  DigitalContractGuid,
}) => {
  useEffect(() => {
    provisionDigitalContractReset();
  }, []);
  return (
    <ConditionalRender
      //@ts-ignore
      state={provisionDigitalContractState}
      success={ProvisionDigitalContractSuccess}
      failure={ProvisionDigitalContractFailure}
    >
      <ProvisionDigitalContractForm
        provisionDigitalContractStart={provisionDigitalContractStart}
        DigitalContractGuid={DigitalContractGuid}
      />
    </ConditionalRender>
  );
};

export default ActivateDigitalContract;
