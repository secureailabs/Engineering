import axios, { AxiosResponse } from 'axios';

import { axiosProxy, tokenConfig } from '@app/redux/utils';

import {
  IGetAllEventsStart,
  IPostLeafEventsStart,
  IAuditLogManagerData,
} from './audit-log-manager.typeDefs';

import type { IDefaults } from '@app/redux/typedefs';

export const postLeafEventsAPI = ({
  data,
}: {
  data: IPostLeafEventsStart;
}): Promise<
  AxiosResponse<{ data: { doc: IAuditLogManagerData } }> | IDefaults['error']
> =>
  axios
    .post(
      `${axiosProxy()}/api/v1/AuditLogManager/LeafEvents`,
      { ...data },
      tokenConfig()
    )
    .then((res): AxiosResponse<{ data: { doc: IAuditLogManagerData } }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });

export const getAllEventsAPI = (): Promise<
  AxiosResponse<{ data: { doc: IGetAllEventsStart } }> | IDefaults['error']
> =>
  axios
    .get(
      `${axiosProxy()}/api/v1/AuditLogManager/GetListOfEvents`,
      tokenConfig()
    )
    .then((res): AxiosResponse<{ data: { doc: IGetAllEventsStart } }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });
