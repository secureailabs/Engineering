import axios, { AxiosResponse } from 'axios';

import { axiosProxy } from '@APIs/utils';

import {
  TPostAccountManagerStart,
  TPostAccountManagerSuccess,
  TPutUpdateUserStart,
  TPutUpdateUserSuccess,
  TPutUpdatePasswordStart,
  TPutUpdatePasswordSuccess,
  TPutUpdateAccessRightsStart,
  TPutUpdateAccessRightsSuccess,
  TGetAllAccountManagersSuccess,
  TGetAccountManagerSuccess,
  TGetAllAccountManagersStart,
  TGetAccountManagerStart,
  TDeleteAccountManagerSuccess,
  TDeleteAccountManagerStart,
  TPutAccountManagerSuccess,
  TPutAccountManagerStart,
} from './accountManager.typeDefs';

import type { IDefaults } from '@APIs/typedefs';

export const postAccountManagerAPI = ({
  data,
}: {
  data: TPostAccountManagerStart;
}): Promise<
  AxiosResponse<{ data: TPostAccountManagerSuccess }> | IDefaults['error']
> =>
  axios
    .post(
      `${axiosProxy()}/api/v1/AccountManager/Admin/RegisterUser`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TPostAccountManagerSuccess }> => {
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

export const putUpdateUserAPI = ({
  data,
}: {
  data: TPutUpdateUserStart;
}): Promise<
  AxiosResponse<{ data: TPutUpdateUserSuccess }> | IDefaults['error']
> =>
  axios
    .put(
      `${axiosProxy()}/api/v1/AccountManager/Update/User`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TPutUpdateUserSuccess }> => {
        // The backend sometimes returns status 200 or 204 even when the contract couldnt be registered
        console.log(res);
        if (res.data.Status != 200) {
          throw new Error('Backend didnt return 201');
        }
        return res;
      }
    )
    .catch((err): IDefaults['error'] => {
      throw err;
    });

export const putUpdatePasswordAPI = ({
  data,
}: {
  data: TPutUpdatePasswordStart;
}): Promise<
  AxiosResponse<{ data: TPutUpdatePasswordSuccess }> | IDefaults['error']
> =>
  axios
    .patch(
      `${axiosProxy()}/api/v1/AuthenticationManager/User/Password`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TPutUpdatePasswordSuccess }> => {
        // The backend sometimes returns status 200 or 204 even when the contract couldnt be registered
        console.log(res);
        if (res.data.Status != 200) {
          throw new Error('Backend didnt return 201');
        }
        return res;
      }
    )
    .catch((err): IDefaults['error'] => {
      throw err;
    });

export const putUpdateAccessRightsAPI = ({
  data,
}: {
  data: TPutUpdateAccessRightsStart;
}): Promise<
  AxiosResponse<{ data: TPutUpdateAccessRightsSuccess }> | IDefaults['error']
> =>
  axios
    .put(
      `${axiosProxy()}/api/v1/AccountManagerManager/DataOwner/`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TPutUpdateAccessRightsSuccess }> => {
        // The backend sometimes returns status 200 or 204 even when the contract couldnt be registered
        console.log(res);
        if (res.data.Status != 200) {
          throw new Error('Backend didnt return 201');
        }
        return res;
      }
    )
    .catch((err): IDefaults['error'] => {
      throw err;
    });

export const getAccountManagerAPI = ({
  data,
}: {
  data: TGetAccountManagerStart;
}): Promise<
  AxiosResponse<{ data: TGetAccountManagerSuccess }> | IDefaults['error']
> =>
  axios
    .get(
      `${axiosProxy()}/api/v1/AccountManagerManager/PullAccountManager?AccountManagerGuid=${data.AccountManagerGuid
      }`,
      {
        withCredentials: true,
      }
    )
    .then((res): AxiosResponse<{ data: TGetAccountManagerSuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });

export const getAllAccountManagersAPI = ({
  data,
}: {
  data: TGetAllAccountManagersStart;
}): Promise<
  AxiosResponse<{ data: TGetAllAccountManagersSuccess }> | IDefaults['error']
> => {
  console.log('api data');
  console.log(data)
  return axios
    .get(`${axiosProxy()}/api/v1/AccountManager/Organization/Users`, {
      params: data,
      withCredentials: true,
    })
    .then((res): AxiosResponse<{ data: TGetAllAccountManagersSuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });
}

export const deleteAccountManagerAPI = ({
  data,
}: {
  data: TDeleteAccountManagerStart;
}): Promise<
  AxiosResponse<{ data: TDeleteAccountManagerSuccess }> | IDefaults['error']
> => {
  console.log('deleteaccountmanagerstart API');
  return axios
    .delete(`${axiosProxy()}/api/v1/AccountManager/Remove/User`, {
      params: data,
      withCredentials: true,
    })
    .then((res): AxiosResponse<{ data: TDeleteAccountManagerSuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });
};

export const putAccountManagerAPI = ({
  data,
}: {
  data: TPutAccountManagerStart;
}): Promise<
  AxiosResponse<{ data: TPutAccountManagerSuccess }> | IDefaults['error']
> => {
  return axios
    .put(`${axiosProxy()}/api/v1/AccountManager/Update/RecoverUser`, data, {
      withCredentials: true,
    })
    .then((res): AxiosResponse<{ data: TPutAccountManagerSuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });
};
