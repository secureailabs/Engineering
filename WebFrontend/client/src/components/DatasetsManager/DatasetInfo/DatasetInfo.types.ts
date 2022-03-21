import { IDefaults } from '@redux/typedefs';
import { TGetDatasetSuccess } from '@redux/dataset/dataset.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';

export type TDatasetInfoSuccess = {
  getDatasetData: TGetDatasetSuccess | null;
  userData: IUserData;
};

export type TDatasetInfo = {
  getDatasetStart(key: string): void;
  getDatasetReset(): void;
  getDatasetState: IDefaults['state'];
  getDatasetData: TGetDatasetSuccess | null;
  datasetID: string;
  userData: IUserData;
};
