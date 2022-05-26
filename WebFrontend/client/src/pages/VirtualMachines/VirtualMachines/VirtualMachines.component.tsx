import React, { useEffect, useState } from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TVirtualMachinesProps } from './VirtualMachines.types';
import { CSSTransition } from 'react-transition-group';

import VirtualMachinesSuccess from './VirtualMachines.success';
import VirtualMachinesFailure from './VirtualMachines.failure';
import Spinner from '@components/Spinner/SpinnerOnly.component';
import { HiArrowLeft } from 'react-icons/hi';
import VirtualMachineInfo from '@components/VirtualMachineInfo';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

const VirtualMachines: React.FC<TVirtualMachinesProps> = ({
  getAllVirtualMachinesReset,
  getAllVirtualMachinesStart,
  getAllVirtualMachinesState,
  getAllVirtualMachinesData,
  userData,
}) => {
  // useEffect(() => {
  //   getAllVirtualMachinesReset();
  //   getAllVirtualMachinesStart();
  // }, []);

  return (
    <StandardContent title="Virtual Machines">
      <ConditionalRender
        //@ts-ignore
        state={getAllVirtualMachinesState}
        success={() => (
          <VirtualMachinesSuccess
            getAllVirtualMachinesData={getAllVirtualMachinesData}
          />
        )}
        failure={VirtualMachinesFailure}
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

export default VirtualMachines;
