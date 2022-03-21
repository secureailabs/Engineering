import React from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TDatasetInfo } from './DatasetInfo.types';

import DatasetInfoSuccess from './DatasetInfo.success';
import DatasetInfoFailure from './DatasetInfo.failure';
import { useEffect } from 'react';

const DatasetInfo: React.FC<TDatasetInfo> = ({
  getDatasetReset,
  getDatasetStart,
  getDatasetState,
  getDatasetData,
  datasetID,
  userData,
}) => {
  useEffect(() => {
    getDatasetReset();
    getDatasetStart(datasetID);
  }, []);

  return (
    <ConditionalRender
      //@ts-ignore
      state={getDatasetState}
      success={() => (
        <DatasetInfoSuccess
          getDatasetData={getDatasetData}
          userData={userData}
        />
      )}
      failure={DatasetInfoFailure}
    >
      <></>
    </ConditionalRender>
  );
};

export default DatasetInfo;
