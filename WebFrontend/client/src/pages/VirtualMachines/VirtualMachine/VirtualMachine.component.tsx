import React from 'react';

import { useForm, SubmitHandler } from 'react-hook-form';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Card from '@secureailabs/web-ui/components/Card';

import { TVirtualMachineProps } from './VirtualMachine.types';

import VirtualMachineSuccess from './VirtualMachine.success';

const VirtualMachine: React.FC<TVirtualMachineProps> = () => {
  const { register, handleSubmit, formState, trigger } = useForm({
    mode: 'onSubmit',
    defaultValues: {},
  });

  const temp_data: TVirtualMachineProps['getVirtualMachineData'] = {
    VirtualMachineGuid: 'uuid2',
    DigitalContractGuid: 'guid',
    DigitalContractTitle: 'Digi',
    DigitalContract: {
      Title: 'temp',
      VersionNumber: '1',
      ContractStage: 1,
      SubscriptionDays: 7,
      Description: 'test',
      DatasetGuid: '123',
      DatasetName: 'name',
      ActivationTime: 0,
      ExpirationTime: 100,
      Eula: '',
      LegalAgreement: '',
      DataOwnerOrganization: '',
      DOOName: 'DOOName',
      ResearcherOrganization: '',
      ROName: '',
      LastActivity: 0,
      ProvisioningStatus: 1,
      //@ts-ignore
      HostForVirtualMachine: 'localhost',
      NumberOfVCPU: 10,
      Note: '',
    },
    //@ts-ignore
    State: 4,
    RegistrationTime: 20,
    HeartbeatBroadcastTime: 10,
    IPAddress: '127.0.0.1',
    NumberOfVCPU: 10,
    HostRegion: 'East',
    StartTime: 1200,
    Note: 'notes',
  };
  return (
    <>
      <StandardContent title="Virtual Machine">
        <VirtualMachineSuccess getVirtualMachineData={temp_data} />
      </StandardContent>
    </>
  );
};

export default VirtualMachine;