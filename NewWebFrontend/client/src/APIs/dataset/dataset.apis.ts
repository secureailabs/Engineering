import axios, { AxiosResponse } from 'axios';

import { axiosProxy, tokenConfig } from '@APIs/utils';

import {
  TGetAllDatasetsStart,
  TGetAllDatasetsSuccess,
  TGetDatasetSuccess,
  TGetDatasetStart,
} from './dataset.typeDefs';

export const getDatasetAPI = async (data: TGetDatasetStart): Promise<TGetDatasetSuccess> => {
  const res = await axios.get<TGetDatasetSuccess>
    (`${axiosProxy()}/api/v1/dataset-versions/${data.dataset_id}`,
      {
        data: data,
        withCredentials: true,
      });
  return res.data;
}

export const getAllDatasetsAPI = async({data} : {data: TGetAllDatasetsStart}): Promise<TGetAllDatasetsSuccess['datasets']> => {
  const res = await axios.get<TGetAllDatasetsSuccess>
    (`${axiosProxy()}/api/v1/dataset-versions`,
      {
        data: data,
        withCredentials: true,
      });
  return res.data.datasets;
}
