import {
  TGetDatasetVersionSuccess,
  TGetDatasetVersionStart,
} from '@redux/dataset/dataset.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TDatasetVersionProps = {
  getDatasetVersionStart(data: TGetDatasetVersionStart): void;
  getDatasetVersionReset(): void;
  getDatasetVersionState: IDefaults['state'];
  getDatasetVersionData: TGetDatasetVersionSuccess;
  userData: IUserData;
};

export type TDatasetVersionSuccessProps = {
  getDatasetVersionData: TGetDatasetVersionSuccess;
};
