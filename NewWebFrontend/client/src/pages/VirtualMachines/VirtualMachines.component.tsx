import React from 'react';
import Spinner from '@components/Spinner';

import { ConditionalRender } from '@components/ConditionalRenderRQuery';
import { TVirtualMachinesProps } from './VirtualMachines.types';

import VirtualMachinesSuccess from './VirtualMachines.success';
import VirtualMachinesFailure from './VirtualMachines.failure';
// import Spinner from '@components/Spinner/SpinnerOnly.component';
// import { HiArrowLeft } from 'react-icons/hi';

import StandardContent from '@secureailabs/web-ui/components/StandardContent';

const VirtualMachines: React.FC<TVirtualMachinesProps> = ({status, getAllVirtualMachinesData, error, userData}) => {

  return (
    <StandardContent title="Computational Resources">
      <ConditionalRender
        status={status}
        success={() =>
          <VirtualMachinesSuccess getAllVirtualMachinesData={getAllVirtualMachinesData} userData={userData} />
        }
        failure={() =>
          <VirtualMachinesFailure error={error} />
        }>
        <Spinner />
      </ConditionalRender>
    </StandardContent>
  );
};

export default VirtualMachines;
