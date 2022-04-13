import React from 'react';

import { TDatasetFailure } from './Dataset.types';

const DatasetFailure: React.FC<TDatasetFailure> = ({ error }) => {
  if(error){
    return <></>;
}
return <>An unkown error has occured</>;
};

export default DatasetFailure;
