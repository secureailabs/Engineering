import React from 'react';

import { useForm, SubmitHandler } from 'react-hook-form';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';

import { ConditionalRender } from '@components/ConditionalRender';
import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Card from '@secureailabs/web-ui/components/Card';

import Spinner from '@components/Spinner/SpinnerOnly.component';
import { TAzureTemplateProps } from './AzureTemplate.types';

import AzureTemplateSuccess from './AzureTemplate.success';

const AzureTemplate: React.FC<TAzureTemplateProps> = () => {
  const { register, handleSubmit, formState, trigger } = useForm({
    mode: 'onSubmit',
    defaultValues: {},
  });

  const temp_data: TAzureTemplateProps['getAzureTemplateData'] = {
    Template: {
      TemplateGuid: 'uuid1',
      Name: 'Name',
      Description: 'Description',
      SubscriptionID: 'SubscriptionID',
      TenantID: 'TenantID',
      ApplicationID: 'ApplicationID',
      ResourceGroup: 'ResourceGroup',
      VirtualNetwork: 'VirtualNetwork',
      HostRegion: 'HostRegion',
      VirtualMachineImage: 'VirtualMachineImage',
      State: 1,
      Note: 'Note',
    },
  };
  return (
    <>
      <StandardContent title="Azure Template">
        <ConditionalRender
          //@ts-ignore
          state={'success'}
          success={() => (
            <AzureTemplateSuccess getAzureTemplateData={temp_data} />
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

export default AzureTemplate;
