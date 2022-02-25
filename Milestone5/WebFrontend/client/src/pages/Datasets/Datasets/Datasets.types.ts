import { TGetAllDatasetsSuccess } from '@redux/dataset/dataset.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TDatasetsProps = {
  getAllDatasetsStart(): void;
  getAllDatasetsReset(): void;
  getAllDatasetsState: IDefaults['state'];
  getAllDatasetsData: TGetAllDatasetsSuccess;
};

export type TDatasetsSuccessProps = {
  getAllDatasetsData: TGetAllDatasetsSuccess;
};
