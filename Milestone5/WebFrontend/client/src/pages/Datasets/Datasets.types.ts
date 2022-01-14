import { TGetAllDatasetsSuccess } from '@redux/dataset/dataset.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TDatasetsProps = {
  getAllDatasetsStart(): void;
  getAllDatasetsReset(): void;
  getAllDatasetsState: IDefaults['state'];
  getAllDatasetsData: TGetAllDatasetsSuccess;
};

export type TDatasetsSuccessProps = {
  setDatasetID(data: string | null): void;

  getAllDatasetsData: TGetAllDatasetsSuccess;
};
