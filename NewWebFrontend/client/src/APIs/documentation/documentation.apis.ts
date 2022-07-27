import {
  TGetAllDocumentationSuccess
} from './documentation.typeDefs';

import Documentation_data from './documentation.data';

export const getAllDocumentationAPIDemo = async(): Promise<TGetAllDocumentationSuccess['documentation']> => {
  return Documentation_data.documentation;
}
