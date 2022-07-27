import {
  TGetAllDocumentationsSuccess
} from './documentation.typeDefs';

import Documentation_data from './documentation.data';

export const getAllDocumentationsAPIDemo = async(): Promise<TGetAllDocumentationsSuccess['documentations']> => {
  return Documentation_data.documentations;
}
