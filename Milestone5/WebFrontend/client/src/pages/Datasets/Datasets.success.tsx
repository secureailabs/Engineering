import React, { useState } from 'react';

import { TDatasetsSuccessProps } from './Datasets.types';

import DatasetList from '@components/DatasetsManager/DatasetList';

const DatasetsSuccess: React.FC<TDatasetsSuccessProps> = ({
  getAllDatasetsData,
  setDatasetID,
}) => {
  const parsedData = Object.entries(getAllDatasetsData.Datasets).map(
    ([key, value]) => {
      return {
        key,
        ...value,
        PublishDate: new Date(value.PublishDate * 1000).toLocaleDateString(
          'en-US',
          {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
          }
        ),
      };
    }
  )
  .sort((elem1, elem2) => elem1.DatasetName.localeCompare(elem2.DatasetName));

  return <DatasetList setDatasetID={setDatasetID} Datasets={parsedData} />;
};

export default DatasetsSuccess;
