import {
  TGetDatasetVersionSuccess,
  TGetDatasetVersionStart,
  TGetDatasetSuccess,
} from '@app/redux/dataset/dataset.typeDefs';
import { IUserData } from '@app/redux/user/user.typeDefs';
import { IDefaults } from '@app/redux/typedefs';
import { AxiosError } from 'axios';

export type TDatasetVersionProps = {
  getDatasetVersionStart(data: TGetDatasetVersionStart): void;
  getDatasetVersionReset(): void;
  getDatasetVersionState: IDefaults['state'];
  getDatasetVersionData: TGetDatasetVersionSuccess;
  getDatasetData: TGetDatasetSuccess;
  userData: IUserData;
};

export type TDatasetVersionSuccessProps = {
  getDatasetVersionData: TGetDatasetVersionSuccess['Dataset'];

  getDatasetData: TGetDatasetSuccess['Dataset'];
};

export type TDatasetVersionFailure = {
  error: AxiosError<any> | null
}