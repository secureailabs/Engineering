import React from 'react';

import { useForm, SubmitHandler } from 'react-hook-form';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';
import Button from '@secureailabs/web-ui/components/Button';
import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Card from '@secureailabs/web-ui/components/Card';
import stageNumberToString from '@utils/stageNumberToString';

import { TAzureTemplateSuccessProps } from './AzureTemplate.types';
import getPartnerOrg from '@utils/getPartnerOrg';

import Margin from '@secureailabs/web-ui/components/Margin';

const AzureTemplateSuccess: React.FC<TAzureTemplateSuccessProps> = ({
  getAzureTemplateData,
}) => {
  const { register, handleSubmit, formState, trigger } = useForm({
    mode: 'onSubmit',
    defaultValues: {
      ...getAzureTemplateData.Template,
    },
  });
  return (
    <>
      <Card primaryText="">
        <div className="form-double">
          <FormFieldsRenderer
            register={register}
            formState={formState}
            fields={{
              Name: {},
              HostRegion: {},
              SubscriptionID: {},
              TenantID: {},
              ApplicationID: {},
              ResourceGroup: {},
              VirtualNetwork: {},
              NetworkSecurityGroup: {},
              VirtualMachineImage: {},
            }}
          />
        </div>
      </Card>
      <Margin size={8} />
      <div className="button-container">
        <Button button_type="primary" full={false}>
          Update Azure Template
        </Button>
        <Button button_type="secondary" full={false}>
          Delete Azure Template
        </Button>
      </div>
    </>
  );
};

export default AzureTemplateSuccess;
