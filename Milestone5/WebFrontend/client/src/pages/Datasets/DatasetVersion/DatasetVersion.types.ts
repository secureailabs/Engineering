import {
  TGetDatasetVersionSuccess,
  TGetDatasetVersionStart,
  TGetDatasetSuccess,
} from '@redux/dataset/dataset.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TDatasetVersionProps = {
  getDatasetVersionStart(data: TGetDatasetVersionStart): void;
  getDatasetVersionReset(): void;
  getDatasetVersionState: IDefaults['state'];
  getDatasetVersionData: TGetDatasetVersionSuccess;
  getDatasetData: TGetDatasetSuccess;
  userData: IUserData;
};

export type TDatasetVersionSuccessProps = {
  getDatasetVersionData: TGetDatasetVersionSuccess;

  getDatasetData: TGetDatasetSuccess;
};
