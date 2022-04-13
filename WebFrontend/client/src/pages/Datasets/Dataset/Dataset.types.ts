import {
  TGetDatasetSuccess,
  TGetDatasetStart,
} from '@redux/dataset/dataset.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';
import { AxiosError } from 'axios';

export type TDatasetProps = {
  getDatasetStart(data: TGetDatasetStart): void;
  getDatasetReset(): void;
  getDatasetState: IDefaults['state'];
  getDatasetData: TGetDatasetSuccess;
  userData: IUserData;
};

export type TDatasetSuccessProps = {
  getDatasetData: TGetDatasetSuccess['Dataset'];
};

export type TDatasetFailure = {
  error: AxiosError<any> | null
}