//@ts-nocheck
import React from 'react';

import TConditionalRender from './ConditionalRender.types';
import Spinner, { SpinnerOnly } from '@components/Spinner';

const ConditionalRender: React.FC<TConditionalRender> = 
    ({ status, error, success, children }) => {
    if(status === 'error'){
        return <>{error()}</>
        
    }
    if(status === 'success'){
        return <>{success()}</>
    }
    if(status === 'idle'){
        return <>{children}</>
    }
    return <Spinner />
}

export default ConditionalRender;