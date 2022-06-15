import React from 'react';

import { ConditionalRender } from '@components/ConditionalRenderRQuery';
import Spinner from '@components/Spinner/SpinnerOnly.component';

import { TDatasetsProps } from './Datasets.types';

import DatasetsSuccess from './Datasets.success';
import DatasetsFailure from './Datasets.failure';


const Datasets: React.FC<TDatasetsProps> = ({ status, getAllDatasetsData, error }) => (
  <ConditionalRender
    status={status}
    success={() =>
      <DatasetsSuccess getAllDatasetsData={getAllDatasetsData} />
    }
    failure={() =>
      <DatasetsFailure error={error}/>
    }>
    <Spinner />
  </ConditionalRender>
  );

export default Datasets;
