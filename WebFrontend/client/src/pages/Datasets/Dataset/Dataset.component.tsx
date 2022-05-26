import React from 'react';

import _ from 'lodash';

import Spinner from '@components/Spinner';
import { TDatasetProps } from './Dataset.types';

import DatasetSuccess from './Dataset.success';
import DatasetFailure from "./Dataset.failure";
import { ConditionalRender } from '@components/ConditionalRenderRQuery';


const Dataset: React.FC<TDatasetProps> = ({ status, getDatasetData, error, userData }) => {
  return (
    <ConditionalRender status={status} success={() => <DatasetSuccess getDatasetData={getDatasetData} userData={userData}/>} failure={() => <DatasetFailure error={error}/>}>
      <Spinner />
    </ConditionalRender>
  )

};

export default Dataset;
