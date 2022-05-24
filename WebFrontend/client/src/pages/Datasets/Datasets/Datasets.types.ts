import { TGetAllDatasetsSuccess } from '@app/redux/dataset/dataset.typeDefs';
import { IDefaults } from '@app/redux/typedefs';

import { AxiosError } from 'axios';

export type TDatasetsProps = {

};

export type TDatasetsSuccessProps = {
  getAllDatasetsData: TGetAllDatasetsSuccess['Datasets'];
};


export type TDatasetsFailure = {
  error: AxiosError<any> | null
}