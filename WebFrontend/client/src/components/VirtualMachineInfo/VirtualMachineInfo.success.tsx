import React from 'react';
import { TVirtualMachineInfoSuccess } from './VirtualMachineInfo.types';

import InfoDisplay from '@components/InfoDisplay';
import { TInfoDisplay } from '@components/InfoDisplay/InfoDisplay.types';
const VirtualMachineInfo: React.FC<TVirtualMachineInfoSuccess> = ({
  getVirtualMachineData,
  userData,
  virtualMachineID,
}) => {
  console.log('VIRTUAL MACHINE DATA: ', getVirtualMachineData);

  if (getVirtualMachineData) {
    const data = getVirtualMachineData;

    const info_display: TInfoDisplay['data'] = [
      {
        section_title: 'IP',
        section_data: data.IPAddress,
      },
      {
        section_title: 'Heartbeat Broadcast Time',
        section_data: data.HeartbeatBroadcastTime,
        to_locale_date_string: true,
      },
      {
        section_title: ' Start Time',
        section_data: data.StartTime,
        to_locale_date_string: true,
      },
      {
        section_title: 'Host Region',
        section_data: data.HostRegion,
      },
      {
        section_title: 'Data Owner',
        section_data: data.DigitalContract.DOOName,
      },
      {
        section_title: 'Note',
        section_data: data.Note,
      },
    ];
    return <InfoDisplay data={info_display} />;
  }
  return <></>;
};

export default VirtualMachineInfo;
