import React from 'react';

import { TEditAzureTemplateSuccess } from './EditAzureTemplate.types';

const EditAzureTemplateSuccess: React.FC<TEditAzureTemplateSuccess> = ({
  patchAssociateAzureStart,
  patchAssociateAzureState,
  digitalContractID,
  patchAssociateAzureReset,
  getDigitalContractStart,
}) => {
  React.useEffect(() => {
    if (patchAssociateAzureState === 'success') {
      patchAssociateAzureReset();
      getDigitalContractStart({DigitalContractGuid : digitalContractID});
    }
  }, [patchAssociateAzureState]);
  return <>Form Updated Successfuly</>;
};

export default EditAzureTemplateSuccess;
