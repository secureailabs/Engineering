import React from 'react';
import { TUnifiedRegistriesError } from './UnifiedRegistries.types';

const UnifiedRegistriesFailure: React.FC<TUnifiedRegistriesError> = ({ error }) => {
  if(error){
    return <></>;
  }
  return <>An unkown error has occured</>;
};

export default UnifiedRegistriesFailure;
