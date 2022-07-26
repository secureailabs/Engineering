import { AxiosError } from 'axios';

import { TGetDownloadSuccess } from '@APIs/download/download.typeDefs';
import { IConditionalRender } from '@components/ConditionalRenderRQuery/ConditionalRender/ConditionalRender.types';

export type TDownloadProps = {
  status: IConditionalRender['status'];
  getDownloadData: TGetDownloadSuccess;
  error: AxiosError<any>;
};

export type TDownloadSuccessProps = {
  getDownloadData: TGetDownloadSuccess;
};

export type TDownloadFailure = {
  error: AxiosError<any> | null
}