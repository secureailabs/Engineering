import axios, { AxiosResponse } from 'axios';

import { axiosProxy, tokenConfig } from '@redux/utils';

import {
  TPostDigitalContractStart,
  TPatchAssociateAzureStart,
  TPostDigitalContractSuccess,
  TPatchActivateDigitalContractStart,
  TPatchActivateDigitalContractSuccess,
  TGetAllDigitalContractsSuccess,
  TGetDigitalContractSuccess,
  TGetDigitalContractStart,
  TGetProvisioningStatusStart,
  TGetProvisioningStatusSuccess,
  TProvisionDigitalContractStart,
  TProvisionDigitalContractSuccess,
  TDeprovisionDigitalContractStart,
  TDeprovisionDigitalContractSuccess,
} from './digitalContract.typeDefs';

import type { IDefaults } from '@redux/typedefs';

export const getProvisioningStatusAPI = ({
  data,
}: {
  data: TGetProvisioningStatusStart;
}): Promise<
  AxiosResponse<{ data: TGetProvisioningStatusSuccess }> | IDefaults['error']
> =>
  axios
    .get(
      `${axiosProxy()}/api/v1/DigitalContractManager/GetProvisioningStatus?DigitalContractGuid=${
        data.DigitalContractGuid
      }`,
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TGetProvisioningStatusSuccess }> => {
        return res;
      }
    )
    .catch((err): IDefaults['error'] => {
      throw err;
    });

export const patchAssociateAzureAPI = ({
  data,
}: {
  data: TPatchAssociateAzureStart;
}): Promise<AxiosResponse | IDefaults['error']> =>
  axios
    .patch(
      `${axiosProxy()}/api/v1/DigitalContractManager/AssociateWithAzureTemplate`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse => {
        // The backend sometimes returns status 200 or 204 even when the contract couldnt be registered
        console.log(res);
        // if (res.data.Status != 201) {
        //   throw new Error('Backend didnt return 201');
        // }
        return res;
      }
    )
    .catch((err): IDefaults['error'] => {
      throw err;
    });

export const postDigitalContractAPI = ({
  data,
}: {
  data: TPostDigitalContractStart;
}): Promise<
  AxiosResponse<{ data: TPostDigitalContractSuccess }> | IDefaults['error']
> =>
  axios
    .post(
      `${axiosProxy()}/api/v1/DigitalContractManager/Applications`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TPostDigitalContractSuccess }> => {
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

export const patchActivateDigitalContractAPI = ({
  data,
}: {
  data: TPatchActivateDigitalContractStart;
}): Promise<
  | AxiosResponse<{ data: TPatchActivateDigitalContractSuccess }>
  | IDefaults['error']
> =>
  axios
    .patch(
      `${axiosProxy()}/api/v1/DigitalContractManager/Researcher/Activate`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TPatchActivateDigitalContractSuccess }> => {
        return res;
      }
    )
    .catch((err): IDefaults['error'] => {
      throw err;
    });

export const patchAcceptDigitalContractAPI = ({
  data,
}: {
  data: TPatchActivateDigitalContractStart;
}): Promise<
  | AxiosResponse<{ data: TPatchActivateDigitalContractSuccess }>
  | IDefaults['error']
> =>
  axios
    .patch(
      `${axiosProxy()}/api/v1/DigitalContractManager/DataOwner/Accept`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TPatchActivateDigitalContractSuccess }> => {
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

export const getDigitalContractAPI = ({
  data,
}: {
  data: TGetDigitalContractStart;
}): Promise<
  AxiosResponse<{ data: TGetDigitalContractSuccess }> | IDefaults['error']
> =>
  axios
    .get(
      `${axiosProxy()}/api/v1/DigitalContractManager/PullDigitalContract?DigitalContractGuid=${
        data.DigitalContractGuid
      }`,
      {
        withCredentials: true,
      }
    )
    .then((res): AxiosResponse<{ data: TGetDigitalContractSuccess }> => res)
    .catch((err): IDefaults['error'] => {
      throw err;
    });

export const getAllDigitalContractsAPI = (): Promise<
  AxiosResponse<{ data: TGetAllDigitalContractsSuccess }> | IDefaults['error']
> =>
  axios
    .get(`${axiosProxy()}/api/v1/DigitalContractManager/DigitalContracts`, {
      withCredentials: true,
    })
    .then(
      (res): AxiosResponse<{ data: TGetAllDigitalContractsSuccess }> => {
        console.log('res: ', res);
        return res;
      }
    )
    .catch((err): IDefaults['error'] => {
      throw err;
    });

export const provisionDigitalContractAPI = ({
  data,
}: {
  data: TProvisionDigitalContractStart;
}): Promise<
  AxiosResponse<{ data: TProvisionDigitalContractSuccess }> | IDefaults['error']
> =>
  axios
    .post(
      `${axiosProxy()}/api/v1/DigitalContractManager/Provision`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TPostDigitalContractSuccess }> => {
        // The backend sometimes returns status 204 even when the contract couldnt be registered
        console.log(res);
        if (res.data.Status != 200) {
          throw new Error('Backend didnt return 200');
        }
        return res;
      }
    )
    .catch((err): IDefaults['error'] => {
      throw err;
    });

export const deprovisionDigitalContractAPI = ({
  data,
}: {
  data: TDeprovisionDigitalContractStart;
}): Promise<
  AxiosResponse<{ data: TDeprovisionDigitalContractSuccess }> | IDefaults['error']
> =>
  axios
    .post(
      `${axiosProxy()}/api/v1/DigitalContractManager/Deprovision`,
      { ...data },
      { withCredentials: true }
    )
    .then(
      (res): AxiosResponse<{ data: TDeprovisionDigitalContractSuccess }> => {
        // The backend sometimes returns status 200 or 204 even when the contract couldnt be registered
        console.log(res);
        if (res.data.Status != 200) {
          throw new Error('Backend didnt return 200');
        }
        return res;
      }
    )
    .catch((err): IDefaults['error'] => {
      throw err;
    });