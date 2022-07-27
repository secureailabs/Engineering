import React from 'react';
import Spinner from '@components/Spinner';

import { ConditionalRender } from '@components/ConditionalRenderRQuery';
import { TDocumentationsProps } from './Documentations.types';

import DocumentationSuccess from './Documentations.success';
import DocumentationFailure from './Documentations.failure';

const Documentation: React.FC<TDocumentationsProps> = ({status, getAllDocumentationsData, error}) => (

  <ConditionalRender
    status={status}
    success={() =>
      <DocumentationSuccess getAllDocumentationsData={getAllDocumentationsData} />
    }
    failure={() =>
      <DocumentationFailure error={error}/>
    }>
    <Spinner />
  </ConditionalRender>
  );

export default Documentation;
