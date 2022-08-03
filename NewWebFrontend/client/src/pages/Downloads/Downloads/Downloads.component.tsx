import React from 'react';
import Spinner from '@components/Spinner';

import { ConditionalRender } from '@components/ConditionalRenderRQuery';
import { TDownloadsProps } from './Downloads.types';

import DownloadsSuccess from './Downloads.success';
import DownloadsFailure from './Downloads.failure';

const Downloads: React.FC<TDownloadsProps> = ({status, getAllDownloadsData, error}) => (

  <ConditionalRender
    status={status}
    success={() =>
      <DownloadsSuccess getAllDownloadsData={getAllDownloadsData} />
    }
    failure={() =>
      <DownloadsFailure error={error}/>
    }>
    <Spinner />
  </ConditionalRender>
  );

export default Downloads;
