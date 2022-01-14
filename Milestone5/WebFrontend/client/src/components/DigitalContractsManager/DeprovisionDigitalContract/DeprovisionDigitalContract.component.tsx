import React from 'react';

import { ConditionalRender } from '@components/ConditionalRender';

import { TDeprovisionDigitalContractProps } from './DeprovisionDigitalContract.types';

import DeprovisionDigitalContractForm from './DeprovisionDigitalContract.form';

import DeprovisionDigitalContractSuccess from './DeprovisionDigitalContract.success';
import DeprovisionDigitalContractFailure from './DeprovisionDigitalContract.failure';
import { useEffect } from 'react';

const DeprovisionDigitalContract: React.FC<TDeprovisionDigitalContractProps> = ({
  deprovisionDigitalContractState,
  deprovisionDigitalContractStart,
  deprovisionDigitalContractReset,
  DigitalContractGuid,
}) => {
  useEffect(() => {
    deprovisionDigitalContractReset();
  }, []);
  return (
    <ConditionalRender
      //@ts-ignore
      state={deprovisionDigitalContractState}
      success={DeprovisionDigitalContractSuccess}
      failure={DeprovisionDigitalContractFailure}
    >
      <DeprovisionDigitalContractForm
        deprovisionDigitalContractStart={deprovisionDigitalContractStart}
        DigitalContractGuid={DigitalContractGuid}
      />
    </ConditionalRender>
  );
};

export default DeprovisionDigitalContract;
