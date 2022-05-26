import React, { useEffect } from 'react';

import _ from 'lodash';

import axios, { AxiosError } from 'axios';

import Spinner from '@components/Spinner';
import { TDatasetProps } from './Dataset.types';

import DatasetSuccess from './Dataset.success';
import DatasetFailure from "./Dataset.failure";
import { TGetDatasetSuccess } from '@APIs/dataset/dataset.typeDefs';
import { useParams } from 'react-router';
import { useQuery } from 'react-query';
import { ConditionalRender } from '@components/ConditionalRenderRQuery';


const Dataset: React.FC<TDatasetProps> = ({ status, getDatasetData, error, userData }) => {
  return (
    <ConditionalRender status={status} success={() => <DatasetSuccess getDatasetData={getDatasetData} userData={userData}/>} failure={() => <DatasetFailure error={error}/>}>
      <Spinner />
    </ConditionalRender>
  )

};

export default Dataset;
