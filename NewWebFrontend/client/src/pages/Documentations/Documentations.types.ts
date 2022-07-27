import { AxiosError } from 'axios';

import { IConditionalRender } from '@components/ConditionalRenderRQuery/ConditionalRender/ConditionalRender.types';
import { TGetAllDocumentationsSuccess } from '@APIs/documentation/documentation.typeDefs';

export type TDocumentationsProps = {
  status: IConditionalRender['status'];
  getAllDocumentationsData: TGetAllDocumentationsSuccess['documentations'];
  error: AxiosError<any>;
};

export type TDocumentationsFailureProps = {
  error: AxiosError<any>;
}

export type TDocumentationsSuccessProps = {
  getAllDocumentationsData: TGetAllDocumentationsSuccess['documentations'];
};
