import React, { useEffect } from 'react';
import { useState } from 'react';

import { TVirtualMachinesSuccessProps } from './VirtualMachines.types';

import VirtualMachineList from '@components/VirtualMachineList';
import _ from 'lodash';
import getDCStage from '@utils/getDCStage';

import getPartnerOrg from '@utils/getPartnerOrg';
import { TGetVirtualMachineSuccess } from '@redux/virtualMachineManager/virtualMachineManager.typeDefs';

const VirtualMachinesSuccess: React.FC<TVirtualMachinesSuccessProps> = ({
  getAllVirtualMachinesData,
  userData,
  stageView,
  setVirtualMachineID,
}) => {
  const parsedData: TGetVirtualMachineSuccess[] = [];
  const temp = Object.entries(getAllVirtualMachinesData)
  .filter((virtualMachines) => {
    if (virtualMachines[1].HostForVirtualMachines === stageView) {
      return true;
    }
  })
  .forEach(([key, value]) => {
    // console.log(value.VirtualMachinesAssociatedWithDc)
    Object.entries(value.VirtualMachinesAssociatedWithDc).forEach(([key, value]) => {
      parsedData.push({
        ...value
      })
    })
  })
  // .map(([key, value]) => {
  //   return {
  //     key,
  //     ...Object.values(value['VirtualMachinesAssociatedWithDc'])[0],
  //   };
  // });

  return (
    <VirtualMachineList
      setVirtualMachineID={setVirtualMachineID}
      // @ts-ignore
      data={parsedData}
    />
  );
};

export default VirtualMachinesSuccess;
