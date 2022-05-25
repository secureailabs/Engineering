import axios, { AxiosResponse } from 'axios';

import { axiosProxy, tokenConfig } from '@APIs/utils';

import {
  TPutOrganizationStart,
  TPutOrganizationSuccess,
  TGetOrganizationSuccess,
  TGetOrganizationStart,
} from './organization.typeDefs';

import type { IDefaults } from '@APIs/typedefs';

export const putOrganizationAPI = ({
  data,
}: {
  data: TPutOrganizationStart;
}): Promise<
  AxiosResponse<{ data: TPutOrganizationSuccess }> | IDefaults['error']
> =>
  axios
    .put(
      `${axiosProxy()}/api/v1/AccountManager/Update/Organization`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TPutOrganizationSuccess }> => {
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

export const getOrganizationAPI = (): Promise<
  | AxiosResponse<{
    data: { OrganizationInformation: TGetOrganizationSuccess };
  }>
  | IDefaults['error']
> =>
  axios
    .get(`${axiosProxy()}/api/v1/AccountManager/Organization/Information`, {
      withCredentials: true,
    })
    .then(
      (
        res
      ): AxiosResponse<{
        data: { OrganizationInformation: TGetOrganizationSuccess };
      }> => res
    )
    .catch((err): IDefaults['error'] => {
      throw err;
    });
