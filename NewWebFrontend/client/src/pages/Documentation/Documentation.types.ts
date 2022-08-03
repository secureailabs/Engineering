import { AxiosError } from 'axios';

import { IConditionalRender } from '@components/ConditionalRenderRQuery/ConditionalRender/ConditionalRender.types';
import { TGetAllDocumentationSuccess } from '@APIs/documentation/documentation.typeDefs';

export type TDocumentationProps = {
  status: IConditionalRender['status'];
  getAllDocumentationData: TGetAllDocumentationSuccess['documentation'];
  error: AxiosError<any>;
};

export type TDocumentationFailureProps = {
  error: AxiosError<any>;
}

export type TDocumentationSuccessProps = {
  getAllDocumentationData: TGetAllDocumentationSuccess['documentation'];
};
