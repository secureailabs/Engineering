import axios, { AxiosResponse } from 'axios';

import { axiosProxy, tokenConfig } from '@APIs/utils';

import {
  TPostUnifiedRegistryStart,
  TPostUnifiedRegistrySuccess,
  TPutUnifiedRegistryStart,
  TPutUnifiedRegistrySuccess,
  TGetAllUnifiedRegistriesSuccess,
  TGetUnifiedRegistrySuccess,
  TGetAllUnifiedRegistriesStart,
  TGetUnifiedRegistryStart,
  TDeleteUnifiedRegistrySuccess,
  TDeleteUnifiedRegistryStart,
} from './unifiedRegistry.types';

import type { IDefaults } from '@APIs/typedefs';

export const postUnifiedRegistryAPI = ({
  data,
}: {
  data: TPostUnifiedRegistryStart;
}): Promise<
  AxiosResponse<{ data: TPostUnifiedRegistrySuccess }> | IDefaults['error']
> =>
  axios
    .post(
      `${axiosProxy()}/api/v1/UnifiedRegistry/Admin/RegisterUser`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TPostUnifiedRegistrySuccess }> => {
        // The backend sometimes returns status 200 or 204 even when the contract couldnt be registered
        console.log(res);
        if (res.data.Status != 201) {
          throw new Error('Backend didnt return 201');
        }
        return res;
      }
    )
    .catch((err): IDefaults['error'] => {
      throw err;
    });
export const getUnifiedRegistryAPI = ({
  data,
}: {
  data: TGetUnifiedRegistryStart;
}): Promise<
  AxiosResponse<{ data: TGetUnifiedRegistrySuccess }> | IDefaults['error']
> =>
  axios
    .get(
      `${axiosProxy()}/api/v1/UnifiedRegistryManager/PullUnifiedRegistry?UnifiedRegistryGuid=${data.ID
      }`,
      {
        withCredentials: true,
      }
    )
    .then((res): AxiosResponse<{ data: TGetUnifiedRegistrySuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });

export const getAllUnifiedRegistriesAPI = ({
  data,
}: {
  data: TGetAllUnifiedRegistriesStart;
}): Promise<
  AxiosResponse<{ data: TGetAllUnifiedRegistriesSuccess }> | IDefaults['error']
> => {
  console.log('api data');
  console.log(data);
  return axios
    .get(`${axiosProxy()}/api/v1/UnifiedRegistry/Organization/Users`, {
      params: data,
      withCredentials: true,
    })
    .then(
      (res): AxiosResponse<{ data: TGetAllUnifiedRegistriesSuccess }> => res
    )
    .catch((err): IDefaults['error'] => {
      throw err;
    });
};

export const deleteUnifiedRegistryAPI = ({
  data,
}: {
  data: TDeleteUnifiedRegistryStart;
}): Promise<
  AxiosResponse<{ data: TDeleteUnifiedRegistrySuccess }> | IDefaults['error']
> => {
  console.log('deleteaccountmanagerstart API');
  return axios
    .delete(`${axiosProxy()}/api/v1/UnifiedRegistry/Remove/User`, {
      params: data,
      withCredentials: true,
    })
    .then((res): AxiosResponse<{ data: TDeleteUnifiedRegistrySuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });
};

export const putUnifiedRegistryAPI = ({
  data,
}: {
  data: TPutUnifiedRegistryStart;
}): Promise<
  AxiosResponse<{ data: TPutUnifiedRegistrySuccess }> | IDefaults['error']
> => {
  return axios
    .put(`${axiosProxy()}/api/v1/UnifiedRegistry/Update/RecoverUser`, data, {
      withCredentials: true,
    })
    .then((res): AxiosResponse<{ data: TPutUnifiedRegistrySuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });
};
