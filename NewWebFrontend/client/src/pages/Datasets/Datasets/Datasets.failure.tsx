import React from 'react';
import { TDatasetFailure } from '../Dataset/Dataset.types';

const DatasetsFailure: React.FC<TDatasetFailure> = () => {
  return (
    <p>There was an error fetching datasets. Please try again later</p>
  );
};

export default DatasetsFailure;
