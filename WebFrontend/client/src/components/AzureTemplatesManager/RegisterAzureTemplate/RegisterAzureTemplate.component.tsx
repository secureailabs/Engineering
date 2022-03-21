import React, { useEffect } from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TRegisterAzureTemplateProps } from './RegisterAzureTemplate.types';

import RegisterAzureTemplateForm from './RegisterAzureTemplate.form';
import RegisterAzureTemplateSuccess from './RegisterAzureTemplate.success';
import RegisterAzureTemplateFailure from './RegisterAzureTemplate.failure';

const RegisterAzureTemplate: React.FC<TRegisterAzureTemplateProps> = ({
  registerAzureTemplateStart,
  registerAzureTemplateReset,
  registerAzureTemplateState,
  listAzureTemplatesReset,
  listAzureTemplatesStart,
  closeModal
}) => {
  useEffect(() => {
    registerAzureTemplateReset();
  }, []);
  return (
    <ConditionalRender
      state={
        registerAzureTemplateState
      }
      success={() => (
        <RegisterAzureTemplateSuccess
          closeModal={() => {
            closeModal();
            listAzureTemplatesReset();
            listAzureTemplatesStart();
          }}
        />
      )}
      failure={() => <RegisterAzureTemplateFailure />}
    >
      <RegisterAzureTemplateForm
        registerAzureTemplateStart={registerAzureTemplateStart}
        registerAzureTemplateReset={registerAzureTemplateReset}
      />
    </ConditionalRender>
  );
};

export default RegisterAzureTemplate;
