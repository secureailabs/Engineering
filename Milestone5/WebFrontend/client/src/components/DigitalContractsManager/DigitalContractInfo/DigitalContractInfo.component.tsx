import React from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TDigitalContractInfo } from './DigitalContractInfo.types';

import DigitalContractInfoSuccess from './DigitalContractInfo.success';
import DigitalContractInfoFailure from './DigitalContractInfo.failure';
import { useEffect, useState } from 'react';

const DigitalContractInfo: React.FC<TDigitalContractInfo> = ({
  getDigitalContractReset,
  getDigitalContractStart,
  getDigitalContractState,
  getDigitalContractData,
  digitalContractID,
  userData,
}) => {
  useEffect(() => {
    getDigitalContractReset();
    getDigitalContractStart(digitalContractID);
  }, []);

  return (
    <ConditionalRender
      //@ts-ignore
      state={getDigitalContractState}
      success={() => (
        <DigitalContractInfoSuccess
          getDigitalContractData={getDigitalContractData}
          userData={userData}
          digitalContractID={digitalContractID}
        />
      )}
      failure={DigitalContractInfoFailure}
    >
      <></>
    </ConditionalRender>
  );
};

export default DigitalContractInfo;
