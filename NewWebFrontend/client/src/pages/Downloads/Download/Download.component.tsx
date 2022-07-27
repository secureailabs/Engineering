import React from 'react';

import _ from 'lodash';

import Spinner from '@components/Spinner';
import { TDownloadProps } from './Download.types';

import DownloadSuccess from './Download.success';
import DownloadFailure from "./Download.failure";
import { ConditionalRender } from '@components/ConditionalRenderRQuery';


const Download: React.FC<TDownloadProps> = ({ status, getDownloadData, error }) => {
  return (
    <ConditionalRender status={status} success={() => <DownloadSuccess getDownloadData={getDownloadData} />} failure={() => <DownloadFailure error={error}/>}>
      <Spinner />
    </ConditionalRender>
  )
};

export default Download;
