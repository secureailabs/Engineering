import axios, { AxiosResponse } from "axios";

import { axiosProxy } from "@redux/utils";

import {
    TRegisterAzureTemplateStart,
    TRegisterAzureTemplateSuccess,
    TListAzureTemplatesSuccess,
    TPullAzureTemplateStart,
    TPullAzureTemplateSuccess,
    TUpdateAzureTemplateStart,
    TUpdateAzureTemplateSuccess,
    TDeleteAzureTemplateStart,
    TDeleteAzureTemplateSuccess,
} from './azureTemplatesManager.typesDefs'

import type { IDefaults } from "@redux/typedefs";

// POST REGISTER TEMPLATE

export const registerAzureTemplateAPI = ({
  data,
}: {
  data: TRegisterAzureTemplateStart;
}): Promise<
  AxiosResponse<{ data: TRegisterAzureTemplateSuccess }> | IDefaults['error']
> =>
  axios
    .post(
      `${axiosProxy()}/api/v1/AzureManager/RegisterTemplate`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TRegisterAzureTemplateSuccess }> => {
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

export const listAzureTemplatesAPI = (
): Promise<
  AxiosResponse<{ data: TListAzureTemplatesSuccess }> | IDefaults['error']
> =>
  axios
    .get(
      `${axiosProxy()}/api/v1/AzureManager/ListTemplates`,
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TListAzureTemplatesSuccess }> => {
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
export const pullAzureTemplateAPI = ({
  data,
}: {
  data: TPullAzureTemplateStart;
}): Promise<
  AxiosResponse<{ data: TPullAzureTemplateSuccess }> | IDefaults['error']
> =>
  axios
    .get(
      `${axiosProxy()}/api/v1/AzureManager/PullTemplate`,
      {
        params: data,
        withCredentials: true,
      }
    )
    .then((res): AxiosResponse<{ data: TPullAzureTemplateSuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });

// PUT UPDATE TEMPLATE
export const updateAzureTemplateAPI = ({
  data,
}: {
  data: TUpdateAzureTemplateStart;
}): Promise<
  AxiosResponse<{ data: TUpdateAzureTemplateSuccess }> | IDefaults['error']
> =>
  axios
    .put(
      `${axiosProxy()}/api/v1/AzureManager/UpdateTemplate`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TUpdateAzureTemplateSuccess }> => {
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