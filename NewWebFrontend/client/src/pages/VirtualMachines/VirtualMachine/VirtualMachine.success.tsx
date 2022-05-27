import React from 'react';

import { useForm, SubmitHandler } from 'react-hook-form';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Card from '@secureailabs/web-ui/components/Card';

// import { TVirtualMachineSuccessProps } from './VirtualMachine.types';

// const VirtualMachineSuccess: React.FC<TVirtualMachineSuccessProps> = ({
const VirtualMachineSuccess: React.FC = () => {
  // const { register, handleSubmit, formState, trigger } = useForm({
  //   mode: 'onSubmit',
  //   defaultValues: {
  //     ...getVirtualMachineData,
  //     DOOName: getVirtualMachineData.DigitalContract.DOOName,
  //   },
  // });
  return (
    <>
      {/* <Card primaryText="">
        {/* <div className="form-double">
          <FormFieldsRenderer
            register={register}
            formState={formState}
            fields={{
              IPAddress: {
                label: 'IP',
                placeholder: 'IP',
                type: 'text',
              },
              HeartbeatBrodcastTime: {
                label: 'Heartbeat Brodcast Time',
                placeholder: 'Heartbeat Brodcast Time',
                type: 'date',
              },
              StartTime: {
                label: 'Start Time',
                placeholder: 'Start Time',
                type: 'date',
              },
              HostRegion: {
                label: 'Host Region',
                placeholder: 'Host Region',
                type: 'text',
              },
              DOOName: {
                label: 'Data Owner',
                placeholder: 'Data Owner',
                type: 'text',
              },
              Note: {
                label: 'Note',
                placeholder: 'Note',
                type: 'text',
              },
            }}
          />
        </div> */}
      {/* </Card> */}
    </>
  );
};

export default VirtualMachineSuccess;
