import React from 'react';

import { ConditionalRender } from '@components/ConditionalRender';

import { TDeleteAzureTemplateProps } from './DeleteAzureTemplate.types';

import DeleteAzureTemplateForm from './DeleteAzureTemplate.form';

import DeleteAzureTemplateSuccess from './DeleteAzureTemplate.success';
import DeleteAzureTemplateFailure from './DeleteAzureTemplate.failure';
import { useEffect } from 'react';

const DeleteAzureTemplate: React.FC<TDeleteAzureTemplateProps> = ({
  deleteAzureTemplateState,
  deleteAzureTemplateStart,
  deleteAzureTemplateReset,
  listAzureTemplatesStart,
  listAzureTemplatesReset,
  closeModal,
  TemplateGuid
}) => {
  useEffect(() => {
    deleteAzureTemplateReset();
  }, []);
  return (
    <ConditionalRender
      //@ts-ignore
      state={deleteAzureTemplateState}
      success={() =>
        <DeleteAzureTemplateSuccess
          closeModal={() => {
            closeModal()
            listAzureTemplatesReset()
            listAzureTemplatesStart()
          }}
        />
      }
      failure={DeleteAzureTemplateFailure}
    >
      <DeleteAzureTemplateForm
        deleteAzureTemplateStart={deleteAzureTemplateStart}
        deleteAzureTemplateReset={deleteAzureTemplateReset}
        TemplateGuid={TemplateGuid}
      />
    </ConditionalRender>
  );
};

export default DeleteAzureTemplate;
