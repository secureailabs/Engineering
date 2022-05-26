import { AxiosError } from 'axios';

import { TGetAllDatasetsSuccess } from '@APIs/dataset/dataset.typeDefs';
import { IConditionalRender } from '@components/ConditionalRenderRQuery/ConditionalRender/ConditionalRender.types';

export type TDatasetsProps = {
  status: IConditionalRender['status'];
  getAllDatasetsData: TGetAllDatasetsSuccess['datasets'];
  error: AxiosError<any>;
};

export type TDatasetsSuccessProps = {
  getAllDatasetsData: TGetAllDatasetsSuccess['datasets'];
};


export type TDatasetsFailure = {
  error: AxiosError<any> | null
}