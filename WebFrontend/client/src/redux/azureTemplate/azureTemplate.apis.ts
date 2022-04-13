import axios, { AxiosResponse } from 'axios';

import { axiosProxy } from '@redux/utils';

import {
  TPostAzureTemplateStart,
  TPostAzureTemplateSuccess,
  TGetAllAzureTemplatesSuccess,
  TGetAzureTemplateStart,
  TGetAzureTemplateSuccess,
  TPutUpdateAzureTemplateStart,
  TPutUpdateAzureTemplateSuccess,
  TDeleteAzureTemplateStart,
  TDeleteAzureTemplateSuccess,
} from './azureTemplate.typesDefs';

import type { IDefaults } from '@redux/typedefs';

// POST REGISTER TEMPLATE

export const postAzureTemplateAPI = ({
  data,
}: {
  data: TPostAzureTemplateStart;
}): Promise<
  AxiosResponse<{ data: TPostAzureTemplateSuccess }> | IDefaults['error']
> =>
  axios
    .post(
      `${axiosProxy()}/api/v1/AzureManager/RegisterTemplate`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TPostAzureTemplateSuccess }> => {
        // // The backend sometimes returns status 200 or 204 even when the contract couldnt be registered
        // console.log(res);
        // if (res.data.Status != 201) {
        //   throw new Error('Backend didnt return 201');
        // }
        return res;
      }
    )
    .catch((err): IDefaults['error'] => {
      throw err;
    });

// GET LIST TEMPLATES

export const getAllAzureTemplatesAPI = (): Promise<
  AxiosResponse<{ data: TGetAllAzureTemplatesSuccess }> | IDefaults['error']
> =>
  axios
    .get(`${axiosProxy()}/api/v1/AzureManager/ListTemplates`, {
      withCredentials: true,
    })
    .then(
      (res): AxiosResponse<{ data: TGetAllAzureTemplatesSuccess }> => {
        // // The backend sometimes returns status 200 or 204 even when the contract couldnt be registered
        // console.log(res);
        // if (res.data.Status != 201) {
        //   throw new Error('Backend didnt return 201');
        // }
        return res;
      }
    )
    .catch((err): IDefaults['error'] => {
      throw err;
    });

// GET PULL TEMPLATE
export const getAzureTemplateAPI = ({
  data,
}: {
  data: TGetAzureTemplateStart;
}): Promise<
  AxiosResponse<{ data: TGetAzureTemplateSuccess }> | IDefaults['error']
> =>
  axios
    .get(`${axiosProxy()}/api/v1/AzureManager/PullTemplate`, {
      params: data,
      withCredentials: true,
    })
    .then((res): AxiosResponse<{ data: TGetAzureTemplateSuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });

// PUT UPDATE TEMPLATE
export const putUpdateAzureTemplateAPI = ({
  data,
}: {
  data: TPutUpdateAzureTemplateStart;
}): Promise<
  AxiosResponse<{ data: TPutUpdateAzureTemplateSuccess }> | IDefaults['error']
> =>
  axios
    .put(
      `${axiosProxy()}/api/v1/AzureManager/UpdateTemplate`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TPutUpdateAzureTemplateSuccess }> => {
        // The backend sometimes returns status 200 or 204 even when the contract couldnt be registered
        console.log(res);
        // if (res.data.Status != 200) {
        //   throw new Error('Backend didnt return 201');
        // }
        return res;
      }
    )
    .catch((err): IDefaults['error'] => {
      throw err;
    });

// DELETE
export const deleteAzureTemplateAPI = ({
  data,
}: {
  data: TDeleteAzureTemplateStart;
}): Promise<
  AxiosResponse<{ data: TDeleteAzureTemplateSuccess }> | IDefaults['error']
> => {
  return axios
    .delete(`${axiosProxy()}/api/v1/AzureManager/DeleteTemplate`, {
      params: data,
      withCredentials: true,
    })
    .then((res): AxiosResponse<{ data: TDeleteAzureTemplateSuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });
};
