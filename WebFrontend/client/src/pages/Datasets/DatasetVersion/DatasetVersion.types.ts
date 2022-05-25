import {
  TGetDatasetVersionSuccess,
  TGetDatasetVersionStart,
  TGetDatasetSuccess,
} from '@APIs/dataset/dataset.typeDefs';
import { IUserData } from '@APIs/user/user.typeDefs';
import { IDefaults } from '@APIs/typedefs';
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