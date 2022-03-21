import React from 'react';

import { ConditionalRender } from '@components/ConditionalRender';

import { TUpdateAzureSecretProps } from './UpdateAzureSecret.types';

import UpdateAzureSecretForm from './UpdateAzureSecret.form';

import UpdateAzureSecretSuccess from './UpdateAzureSecret.success';
import UpdateAzureSecretFailure from './UpdateAzureSecret.failure';
import { useEffect } from 'react';

const UpdateAzureSecret: React.FC<TUpdateAzureSecretProps> = ({
  updateAzureSecretState,
  updateAzureSecretStart,
  updateAzureSecretReset,
  pullAzureTemplateData,
  closeModal,
}) => {
  useEffect(() => {
    updateAzureSecretReset();
  }, []);
  return (
    <ConditionalRender
      //@ts-ignore
      state={updateAzureSecretState}
      success={() => <UpdateAzureSecretSuccess closeModal={closeModal}/>}
      failure={UpdateAzureSecretFailure}
    >
      <UpdateAzureSecretForm
        updateAzureSecretStart={updateAzureSecretStart}
        pullAzureTemplateData={pullAzureTemplateData}
      />
    </ConditionalRender>
  );
};

export default UpdateAzureSecret;
