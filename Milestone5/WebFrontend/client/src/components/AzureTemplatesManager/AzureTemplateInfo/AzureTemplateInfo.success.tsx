import React, { useState } from 'react';
import { TAzureTemplateInfoSuccess } from './AzureTemplateInfo.types';

import UpdateAzureTemplate from '../UpdateAzureTemplate';

const AzureTemplateInfo: React.FC<TAzureTemplateInfoSuccess> = ({ pullAzureTemplateData, slideToPrev }) => {
  if (pullAzureTemplateData) {
    return (
      <div className="templateinfo">
          <UpdateAzureTemplate slideToPrev={slideToPrev} />
      </div>
    );
  }
  return <>There was an error fetching the Azure template information, please try again later.</>;
};

export default AzureTemplateInfo;
