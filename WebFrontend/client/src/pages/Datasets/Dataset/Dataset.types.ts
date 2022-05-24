import {
  TGetDatasetSuccess,
  TGetDatasetStart,
} from '@app/redux/dataset/dataset.typeDefs';
import { IUserData } from '@app/redux/user/user.typeDefs';
import { IDefaults } from '@app/redux/typedefs';
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
  userData: IUserData;
};

export type TDatasetFailure = {
  error: AxiosError<any> | null
}