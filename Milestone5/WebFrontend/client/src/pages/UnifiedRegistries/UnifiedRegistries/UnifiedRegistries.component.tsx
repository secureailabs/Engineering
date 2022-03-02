import React, { useEffect, useState } from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TUnifiedRegistriesProps } from './UnifiedRegistries.types';
import { CSSTransition } from 'react-transition-group';

import UnifiedRegistriesSuccess from './UnifiedRegistries.success';
import UnifiedRegistriesFailure from './UnifiedRegistries.failure';
import Spinner from '@components/Spinner/SpinnerOnly.component';
import { HiArrowLeft } from 'react-icons/hi';
import VirtualMachineInfo from '@components/VirtualMachineInfo';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

const UnifiedRegistries: React.FC<TUnifiedRegistriesProps> = ({
  getAllUnifiedRegistriesReset,
  getAllUnifiedRegistriesStart,
  getAllUnifiedRegistriesState,
  getAllUnifiedRegistriesData,
}) => {
  useEffect(() => {
    getAllUnifiedRegistriesReset();
    getAllUnifiedRegistriesStart();
  }, []);
  return (
    <StandardContent title="Virtual Machines">
      <ConditionalRender
        //@ts-ignore
        state={getAllUnifiedRegistriesState}
        success={() => (
          <UnifiedRegistriesSuccess
            getAllUnifiedRegistriesData={getAllUnifiedRegistriesData}
          />
        )}
        failure={UnifiedRegistriesFailure}
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

export default UnifiedRegistries;
