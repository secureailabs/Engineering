import axios, { AxiosResponse } from 'axios';

import { axiosProxy, tokenConfig } from '@app/redux/utils';

import {
  TPutVirtualMachineStart,
  TPutVirtualMachineSuccess,
  TGetVirtualMachineSuccess,
  TGetVirtualMachineStart,
  TGetAllVirtualMachinesSuccess,
} from './virtualMachineManager.typeDefs';

import type { IDefaults } from '@app/redux/typedefs';

export const putVirtualMachineAPI = ({
  data,
}: {
  data: TPutVirtualMachineStart;
}): Promise<
  AxiosResponse<{ data: TPutVirtualMachineSuccess }> | IDefaults['error']
> =>
  axios
    .put(
      `${axiosProxy()}/api/v1/AccountManager/Update/VirtualMachine`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TPutVirtualMachineSuccess }> => {
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

export const getVirtualMachineAPI = ({
  data,
}: {
  data: TGetVirtualMachineStart;
}): Promise<
  | AxiosResponse<{
      data: { VirtualMachine: TGetVirtualMachineSuccess };
    }>
  | IDefaults['error']
> =>
  axios
    .get(
      `${axiosProxy()}/api/v1/VirtualMachineManager/PullVirtualMachine?VirtualMachineGuid=${
        data.VirtualMachineGuid
      }`,
      {
        withCredentials: true,
      }
    )
    .then(
      (
        res
      ): AxiosResponse<{
        data: { VirtualMachine: TGetVirtualMachineSuccess };
      }> => res
    )
    .catch((err): IDefaults['error'] => {
      throw err;
    });

export const getAllVirtualMachinesAPI = (): Promise<
  | AxiosResponse<{
      data: { VirtualMachines: TGetAllVirtualMachinesSuccess };
    }>
  | IDefaults['error']
> =>
  axios
    .get(`${axiosProxy()}/api/v1/VirtualMachineManager/ListVirtualMachines`, {
      withCredentials: true,
    })
    .then(
      (
        res
      ): AxiosResponse<{
        data: { VirtualMachines: TGetAllVirtualMachinesSuccess };
      }> => res
    )
    .catch((err): IDefaults['error'] => {
      throw err;
    });
