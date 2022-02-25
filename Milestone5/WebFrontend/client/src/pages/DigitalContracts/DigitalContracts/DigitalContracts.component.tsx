import React, { useEffect, useState } from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TDigitalContractsProps } from './DigitalContracts.types';
import { CSSTransition } from 'react-transition-group';

import DigitalContractsSuccess from './DigitalContracts.success';
import DigitalContractsFailure from './DigitalContracts.failure';
import Spinner from '@components/Spinner/SpinnerOnly.component';
import { HiArrowLeft } from 'react-icons/hi';
import VirtualMachineInfo from '@components/VirtualMachineInfo';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

const DigitalContracts: React.FC<TDigitalContractsProps> = ({
  getAllDigitalContractsReset,
  getAllDigitalContractsStart,
  getAllDigitalContractsState,
  getAllDigitalContractsData,
  userData,
}) => {
  useEffect(() => {
    getAllDigitalContractsReset();
    getAllDigitalContractsStart();
  }, []);

  return (
    <StandardContent title="Digital Contracts">
      <ConditionalRender
        //@ts-ignore
        state={getAllDigitalContractsState}
        success={() => (
          <DigitalContractsSuccess
            getAllDigitalContractsData={getAllDigitalContractsData}
            userData={userData}
          />
        )}
        failure={DigitalContractsFailure}
        Loading={
          <>
            <Spinner />
          </>
        }
      >
        <></>
      </ConditionalRender>
    </StandardContent>
  );
};

export default DigitalContracts;
