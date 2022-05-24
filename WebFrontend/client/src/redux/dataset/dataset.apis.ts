import axios, { AxiosResponse } from 'axios';

import { axiosProxy, tokenConfig } from '@app/redux/utils';

import {
  TPostDatasetStart,
  TPostDatasetSuccess,
  TPatchAcceptDatasetStart,
  TPatchAcceptDatasetSuccess,
  TPatchActivateDatasetStart,
  TPatchActivateDatasetSuccess,
  TGetAllDatasetsSuccess,
  TGetDatasetSuccess,
  TGetDatasetStart,
} from './dataset.typeDefs';

import type { IDefaults } from '@app/redux/typedefs';

export const postDatasetAPI = ({
  data,
}: {
  data: TPostDatasetStart;
}): Promise<
  AxiosResponse<{ data: TPostDatasetSuccess }> | IDefaults['error']
> =>
  axios
    .post(
      `${axiosProxy()}/api/v1/DatasetManager/Application`,
      { ...data },
      tokenConfig()
    )
    .then((res): AxiosResponse<{ data: TPostDatasetSuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });

export const getDatasetAPI = ({
  data,
}: {
  data: TGetDatasetStart;
}): Promise<AxiosResponse<{ data: TGetDatasetSuccess }> | IDefaults['error']> =>
  axios
    .get(
      `${axiosProxy()}/api/v1/DatasetManager/PullDataset?DatasetGuid=${
        data.DatasetGuid
      }`,
      {
        withCredentials: true,
      }
    )
    .then((res): AxiosResponse<{ data: TGetDatasetSuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });

export const getAllDatasetsAPI = (): Promise<
  AxiosResponse<{ data: TGetAllDatasetsSuccess }> | IDefaults['error']
> =>
  axios
    .get(`${axiosProxy()}/api/v1/DatasetManager/ListDatasets`, {
      withCredentials: true,
    })
    .then((res): AxiosResponse<{ data: TGetAllDatasetsSuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });
