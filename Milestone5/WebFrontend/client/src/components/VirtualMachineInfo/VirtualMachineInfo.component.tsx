import React from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import Button from '@components/Button';

import { TVirtualMachineInfo } from './VirtualMachineInfo.types';

import VirtualMachineInfoSuccess from './VirtualMachineInfo.success';
import VirtualMachineInfoFailure from './VirtualMachineInfo.failure';
import { useEffect } from 'react';

const VirtualMachineInfo: React.FC<TVirtualMachineInfo> = ({
  getVirtualMachineReset,
  getVirtualMachineStart,
  getVirtualMachineState,
  getVirtualMachineData,
  virtualMachineID,
  userData,
}) => {
  console.log('VIRTUAL MACHINE ID: ', virtualMachineID);
  useEffect(() => {
    getVirtualMachineReset();
    getVirtualMachineStart(virtualMachineID);
  }, []);

  return (
    <>
      <ConditionalRender
        //@ts-ignore
        state={getVirtualMachineState}
        success={() => (
          <VirtualMachineInfoSuccess
            getVirtualMachineData={getVirtualMachineData}
            userData={userData}
            virtualMachineID={virtualMachineID}
          />
        )}
        failure={VirtualMachineInfoFailure}
      >
        <></>
      </ConditionalRender>
      <Button
        size="small"
        onClick={() => {
          getVirtualMachineReset();
          getVirtualMachineStart(virtualMachineID);
        }}
      >
        Refresh
      </Button>
    </>
  );
};

export default VirtualMachineInfo;
