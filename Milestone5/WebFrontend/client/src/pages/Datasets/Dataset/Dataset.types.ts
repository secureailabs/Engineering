import {
  TGetDatasetSuccess,
  TGetDatasetStart,
} from '@redux/dataset/dataset.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TDatasetProps = {
  getDatasetStart(data: TGetDatasetStart): void;
  getDatasetReset(): void;
  getDatasetState: IDefaults['state'];
  getDatasetData: TGetDatasetSuccess;
  userData: IUserData;
};

export type TDatasetSuccessProps = {
  getDatasetData: TGetDatasetSuccess;
};
