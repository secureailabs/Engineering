import React from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TAzureTemplateInfo } from './AzureTemplateInfo.types';

import AzureTemplateInfoSuccess from './AzureTemplateInfo.success';
import AzureTemplateInfoFailure from './AzureTemplateInfo.failure';
import { useEffect } from 'react';

const AzureTemplateInfo: React.FC<TAzureTemplateInfo> = ({
  azureTemplateID,
  pullAzureTemplateData,
  pullAzureTemplateStart,
  pullAzureTemplateReset,
  pullAzureTemplateState,
  slideToPrev,
}) => {
  useEffect(() => {
    pullAzureTemplateReset();
    pullAzureTemplateStart(azureTemplateID);
  }, []);

  return (
    <ConditionalRender
      //@ts-ignore
      state={pullAzureTemplateState}
      success={() => (
        <AzureTemplateInfoSuccess
          pullAzureTemplateData={pullAzureTemplateData}
          slideToPrev={slideToPrev}
        />
      )}
      failure={AzureTemplateInfoFailure}
    >
      <></>
    </ConditionalRender>
  );
};

export default AzureTemplateInfo;
