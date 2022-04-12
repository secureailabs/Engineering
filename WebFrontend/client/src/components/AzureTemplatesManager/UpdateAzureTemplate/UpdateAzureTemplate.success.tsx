import React, { useEffect } from 'react';

import { TUpdateAzureTemplateSuccessProps } from './UpdateAzureTemplate.types';

const UpdateAzureTemplateSuccess = ({
  updateSuccess,
  pullAzureTemplateStart,
  updateAzureTemplateState,
  pullAzureTemplateData,
}: TUpdateAzureTemplateSuccessProps) => {
  useEffect(() => {
    if (updateAzureTemplateState === 'success') {
      updateSuccess(true);
      pullAzureTemplateStart({ TemplateGuid: pullAzureTemplateData.Template.TemplateGuid});
    }
  }, [updateAzureTemplateState]);
  return <>Azure template details updated successfuly</>;
};

export default UpdateAzureTemplateSuccess;
