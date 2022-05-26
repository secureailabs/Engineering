import { AxiosError } from 'axios';

import { IUserData } from '@APIs/user/user.typeDefs';
import { TGetDatasetSuccess } from '@APIs/dataset/dataset.typeDefs';
import { IConditionalRender } from '@components/ConditionalRenderRQuery/ConditionalRender/ConditionalRender.types';

export type TDatasetProps = {
  status: IConditionalRender['status'];
  getDatasetData: TGetDatasetSuccess;
  error: AxiosError<any>;
  userData: IUserData;
};

export type TDatasetSuccessProps = {
  getDatasetData: TGetDatasetSuccess;
  userData: IUserData;
};


export type TDatasetFailure = {
  error: AxiosError<any> | null
}