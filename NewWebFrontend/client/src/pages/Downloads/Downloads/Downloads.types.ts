import { AxiosError } from 'axios';

import { IConditionalRender } from '@components/ConditionalRenderRQuery/ConditionalRender/ConditionalRender.types';
import { TGetAllDownloadsSuccess } from '@APIs/download/download.typeDefs';

export type TDownloadsProps = {
  status: IConditionalRender['status'];
  getAllDownloadsData: TGetAllDownloadsSuccess['downloads'];
  error: AxiosError<any>;
};

export type TDownloadsFailureProps = {
  error: AxiosError<any>;
}

export type TDownloadsSuccessProps = {
  getAllDownloadsData: TGetAllDownloadsSuccess['downloads'];
};
