import React from 'react';

import { TDigitalContractError } from './DigitalContract.types';

const DigitalContractFailure: React.FC<TDigitalContractError> = ({ error }) => {
    if(error){
        return <></>;
    }
    return <>An unkown error has occured</>;
}

export default DigitalContractFailure;