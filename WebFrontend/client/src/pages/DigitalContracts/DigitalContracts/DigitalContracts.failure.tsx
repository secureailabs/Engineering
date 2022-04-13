import React from 'react';

import { TDigitalContractError } from './DigitalContracts.types';

const LoginFailure: React.FC<TDigitalContractError> = ({ error }) => {
  if(error){
    return <></>;
}
return <>An unkown error has occured</>;
};

export default LoginFailure;
