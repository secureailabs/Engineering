import React from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TAzureTemplatesProps } from './AzureTemplates.types';
import AzureTemplatesSuccess from './AzureTemplates.success';
import AzureTemplatesFailure from './AzureTemplates.failure';
import AzureTemplateInfo from '@components/AzureTemplatesManager/AzureTemplateInfo';
import RegisterAzureTemplate from '@components/AzureTemplatesManager/RegisterAzureTemplate';
import { useEffect } from 'react';
import Spinner from '@components/Spinner/SpinnerOnly.component';

import StandardContent from '@secureailabs/web-ui/components/StandardContent';

const AzureTemplatesManager: React.FC<TAzureTemplatesProps> = ({
  getAllAzureTemplatesStart,
  getAllAzureTemplatesReset,
  getAllAzureTemplatesData,
  getAllAzureTemplatesState,
}) => {
  useEffect(() => {
    getAllAzureTemplatesReset();
    getAllAzureTemplatesStart();
    console.log('azure templates updated');
  }, []);

  return (
    <StandardContent title="Azure Templates Manager">
      <ConditionalRender
        //@ts-ignore
        state={getAllAzureTemplatesState}
        success={() => (
          <AzureTemplatesSuccess
            getAllAzureTemplatesData={getAllAzureTemplatesData}
          />
        )}
        failure={AzureTemplatesFailure}
        Loading={
          <>
            <Spinner />
          </>
        }
      >
        <></>
      </ConditionalRender>
    </StandardContent>
  );
};

export default AzureTemplatesManager;
