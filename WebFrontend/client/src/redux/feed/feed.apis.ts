import axios, { AxiosResponse } from 'axios';

import { axiosProxy, tokenConfig } from '@redux/utils';

import {
  TPostFeedStart,
  TPostFeedSuccess,
  TPutFeedStart,
  TPutFeedSuccess,
  TGetAllFeedsSuccess,
  TGetFeedSuccess,
  TGetAllFeedsStart,
  TGetFeedStart,
  TDeleteFeedSuccess,
  TDeleteFeedStart,
} from './feed.types';

import type { IDefaults } from '@redux/typedefs';

export const postFeedAPI = ({
  data,
}: {
  data: TPostFeedStart;
}): Promise<AxiosResponse<{ data: TPostFeedSuccess }> | IDefaults['error']> =>
  axios
    .post(
      `${axiosProxy()}/api/v1/Feed/Admin/RegisterUser`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TPostFeedSuccess }> => {
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
export const getFeedAPI = ({
  data,
}: {
  data: TGetFeedStart;
}): Promise<AxiosResponse<{ data: TGetFeedSuccess }> | IDefaults['error']> =>
  axios
    .get(
      `${axiosProxy()}/api/v1/FeedManager/PullUnifiedRegistry?UnifiedRegistryGuid=${
        data.ID
      }`,
      {
        withCredentials: true,
      }
    )
    .then((res): AxiosResponse<{ data: TGetFeedSuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });

export const getAllFeedsAPI = ({
  data,
}: {
  data: TGetAllFeedsStart;
}): Promise<
  AxiosResponse<{ data: TGetAllFeedsSuccess }> | IDefaults['error']
> => {
  console.log('api data');
  console.log(data);
  return axios
    .get(`${axiosProxy()}/api/v1/Feed/Organization/Users`, {
      params: data,
      withCredentials: true,
    })
    .then((res): AxiosResponse<{ data: TGetAllFeedsSuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });
};

export const deleteFeedAPI = ({
  data,
}: {
  data: TDeleteFeedStart;
}): Promise<
  AxiosResponse<{ data: TDeleteFeedSuccess }> | IDefaults['error']
> => {
  console.log('deleteaccountmanagerstart API');
  return axios
    .delete(`${axiosProxy()}/api/v1/Feed/Remove/User`, {
      params: data,
      withCredentials: true,
    })
    .then((res): AxiosResponse<{ data: TDeleteFeedSuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });
};

export const putFeedAPI = ({
  data,
}: {
  data: TPutFeedStart;
}): Promise<AxiosResponse<{ data: TPutFeedSuccess }> | IDefaults['error']> => {
  return axios
    .put(`${axiosProxy()}/api/v1/Feed/Update/RecoverUser`, data, {
      withCredentials: true,
    })
    .then((res): AxiosResponse<{ data: TPutFeedSuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });
};
