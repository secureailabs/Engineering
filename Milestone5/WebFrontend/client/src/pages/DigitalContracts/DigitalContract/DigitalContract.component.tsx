import React from 'react';

import { useForm, SubmitHandler } from 'react-hook-form';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

import { ConditionalRender } from '@components/ConditionalRender';
import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Card from '@secureailabs/web-ui/components/Card';

import Spinner from '@components/Spinner/SpinnerOnly.component';
import { TDigitalContractProps } from './DigitalContract.types';

import DigitalContractSuccess from './DigitalContract.success';

const DigitalContract: React.FC<TDigitalContractProps> = () => {
  const { register, handleSubmit, formState, trigger } = useForm({
    mode: 'onSubmit',
    defaultValues: {},
  });

  const temp_data: TDigitalContractProps['getDigitalContractData'] = {
    DigitalContractGuid: 'uuid2',
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
      HostForDigitalContract: 'localhost',
      NumberOfVCPU: 10,
      Note: '',
    },
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
      <StandardContent title="Digital Contract">
        <ConditionalRender
          //@ts-ignore
          state={'success'}
          success={() => (
            <DigitalContractSuccess getDigitalContractData={temp_data} />
          )}
          failure={<>Failure</>}
          Loading={
            <>
              <Spinner />
            </>
          }
        >
          <></>
        </ConditionalRender>
      </StandardContent>
    </>
  );
};

export default DigitalContract;
