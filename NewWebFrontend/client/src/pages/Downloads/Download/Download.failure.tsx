import React from 'react';

import { TDownloadFailure } from './Download.types';

const DownloadFailure: React.FC<TDownloadFailure> = ({ error }) => {
  if(error){
    return <></>;
}
return <>An unknown error has occured</>;
};

export default DownloadFailure;
