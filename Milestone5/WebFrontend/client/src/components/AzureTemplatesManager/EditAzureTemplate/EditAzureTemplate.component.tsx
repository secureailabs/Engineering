import React from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TEditAzureTemplate } from './EditAzureTemplate.types';

import EditAzureTemplateSuccess from './EditAzureTemplate.success';
import EditAzureTemplateForm from './EditAzureTemplate.form';
import DigitalContractInfoFailure from './EditAzureTemplate.failure';
import { useEffect } from 'react';

const EditAzureTemplate: React.FC<TEditAzureTemplate> = ({
  patchAssociateAzureStart,
  patchAssociateAzureReset,
  patchAssociateAzureState,
  digitalContractID,
  getDigitalContractStart,
}) => {
  useEffect(() => {
    patchAssociateAzureReset();
  }, []);

  return (
    <ConditionalRender
      //@ts-ignore
      state={patchAssociateAzureState}
      success={() => (
        <EditAzureTemplateSuccess
          digitalContractID={digitalContractID}
          patchAssociateAzureStart={patchAssociateAzureStart}
          getDigitalContractStart={getDigitalContractStart}
          patchAssociateAzureState={patchAssociateAzureState}
          patchAssociateAzureReset={patchAssociateAzureReset}
        />
      )}
      failure={DigitalContractInfoFailure}
    >
      <>
        <EditAzureTemplateForm
          digitalContractID={digitalContractID}
          patchAssociateAzureStart={patchAssociateAzureStart}
        />
      </>
    </ConditionalRender>
  );
};

export default EditAzureTemplate;
