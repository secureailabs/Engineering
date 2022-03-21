import React, { useEffect, useState } from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TUpdateAzureTemplateProps } from './UpdateAzureTemplate.types';

import UpdateAzureTemplateForm from './UpdateAzureTemplate.form';
import UpdateAzureTemplateSuccess from './UpdateAzureTemplate.success';
import UpdateAzureTemplateFailure from './UpdateAzureTemplate.failure';

const UpdateOrganization: React.FC<TUpdateAzureTemplateProps> = ({
  updateAzureTemplateReset,
  updateAzureTemplateStart,
  updateAzureTemplateState,
  pullAzureTemplateData,
  pullAzureTemplateStart,
  slideToPrev,
}) => {
  const [success, updateSuccess] = useState(false);
  useEffect(() => {
    updateAzureTemplateReset();
  }, []);
  return (
    <ConditionalRender
      //@ts-ignore
      state={updateAzureTemplateState}
      success={() => (
        <UpdateAzureTemplateSuccess
          updateSuccess={updateSuccess}
          pullAzureTemplateStart={pullAzureTemplateStart}
          updateAzureTemplateStart={updateAzureTemplateStart}
          updateAzureTemplateState={updateAzureTemplateState}
          pullAzureTemplateData={pullAzureTemplateData}
        />
      )}
      failure={UpdateAzureTemplateFailure}
    >
      <UpdateAzureTemplateForm
        pullAzureTemplateData={pullAzureTemplateData}
        updateAzureTemplateReset={updateAzureTemplateReset}
        updateAzureTemplateStart={updateAzureTemplateStart}
        slideToPrev={slideToPrev}
      />
    </ConditionalRender>
  );
};

export default UpdateOrganization;
