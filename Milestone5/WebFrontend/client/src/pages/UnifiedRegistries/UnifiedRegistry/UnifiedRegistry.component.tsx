import React, { useEffect } from 'react';

import { TUnifiedRegistryProps } from './UnifiedRegistry.types';

import UnifiedRegistrySuccess from './UnifiedRegistry.success';
import UnifiedRegistryFailure from './UnifiedRegistry.failure';

import { ConditionalRender } from '@components/ConditionalRender';
import Spinner from '@components/Spinner/SpinnerOnly.component';
import StandardContent from '@secureailabs/web-ui/components/StandardContent';
const UnifiedRegistry: React.FC<TUnifiedRegistryProps> = ({
  getUnifiedRegistryReset,
  getUnifiedRegistryStart,
  getUnifiedRegistryState,
  getUnifiedRegistryData,
}) => {
  useEffect(() => {
    getUnifiedRegistryReset();
    getUnifiedRegistryStart('uuid1');
  }, []);
  return (
    <StandardContent title="Unified Registries">
      <ConditionalRender
        //@ts-ignore
        state={getUnifiedRegistryState}
        success={() => (
          <UnifiedRegistrySuccess
            getUnifiedRegistryData={getUnifiedRegistryData}
          />
        )}
        failure={UnifiedRegistryFailure}
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
export default UnifiedRegistry;
