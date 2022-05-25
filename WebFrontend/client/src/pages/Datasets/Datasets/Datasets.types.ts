import { TGetAllDatasetsSuccess } from '@APIs/dataset/dataset.typeDefs';
import { IDefaults } from '@APIs/typedefs';

import { AxiosError } from 'axios';

export type TDatasetsProps = {

};

export type TDatasetsSuccessProps = {
  getAllDatasetsData: TGetAllDatasetsSuccess['Datasets'];
};


export type TDatasetsFailure = {
  error: AxiosError<any> | null
}