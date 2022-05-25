import axios, { AxiosResponse } from 'axios';

import { axiosProxy, tokenConfig } from '@APIs/utils';

import {
  TGetAllDatasetsStart,
  TGetAllDatasetsSuccess,
  TGetDatasetSuccess,
  TGetDatasetStart,
} from './dataset.typeDefs';

import type { IDefaults } from '@APIs/typedefs';

export const getDatasetAPI = ({
  data,
}: {
  data: TGetDatasetStart;
}): Promise<AxiosResponse<{ data: TGetDatasetSuccess }> | IDefaults['error']> =>
  axios
    .get(
      `${axiosProxy()}/api/v1/DatasetManager/PullDataset?DatasetGuid=${data.dataset_id}`,
      {
        data: data,
        withCredentials: true,
      }
    )
    .then((res): AxiosResponse<{ data: TGetDatasetSuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });

export const getAllDatasetsAPI = async({data} : {data: TGetAllDatasetsStart}): Promise<TGetAllDatasetsSuccess['datasets']> => {
  const res = await axios.get<TGetAllDatasetsSuccess>
    (`${axiosProxy()}/api/v1/datasets`,
      {
        data: data,
        withCredentials: true,
      });
  return res.data.datasets;
}
