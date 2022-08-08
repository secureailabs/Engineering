import React from 'react';
import Spinner from '@components/Spinner';

import { ConditionalRender } from '@components/ConditionalRenderRQuery';
import { TDocumentationProps } from './Documentation.types';

import DocumentationSuccess from './Documentation.success';
import DocumentationFailure from './Documentation.failure';

const Documentation: React.FC<TDocumentationProps> = ({status, getAllDocumentationData, error}) => (

  <ConditionalRender
    status={status}
    success={() =>
      <DocumentationSuccess getAllDocumentationData={getAllDocumentationData} />
    }
    failure={() =>
      <DocumentationFailure error={error}/>
    }>
    <Spinner />
  </ConditionalRender>
  );

export default Documentation;
