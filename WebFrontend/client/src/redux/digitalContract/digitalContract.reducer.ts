// tslint:disable: no-null-null-union
import { createReducer } from 'typesafe-actions';

import {
  // GET ALL
  getAllDigitalContractsFailure,
  getAllDigitalContractsReset,
  getAllDigitalContractsStart,
  getAllDigitalContractsSuccess,
  // GET ONE
  getDigitalContractFailure,
  getDigitalContractReset,
  getDigitalContractStart,
  getDigitalContractSuccess,
  // PATCH ACTIVATE
  patchActivateDigitalContractFailure,
  patchActivateDigitalContractReset,
  patchActivateDigitalContractStart,
  patchActivateDigitalContractSuccess,
  // PATCH ACCEPT
  patchAcceptDigitalContractFailure,
  patchAcceptDigitalContractReset,
  patchAcceptDigitalContractStart,
  patchAcceptDigitalContractSuccess,
  // POST
  postDigitalContractFailure,
  postDigitalContractReset,
  postDigitalContractStart,
  postDigitalContractSuccess,
  // PATCH ASSOCIATE AZURE
  patchAssociateAzureFailure,
  patchAssociateAzureReset,
  patchAssociateAzureStart,
  patchAssociateAzureSuccess,
  // GET PROVISIONING STATUS
  getProvisioningStatusFailure,
  getProvisioningStatusReset,
  getProvisioningStatusStart,
  getProvisioningStatusSuccess,
  // POST PROVISION
  provisionDigitalContractFailure,
  provisionDigitalContractReset,
  provisionDigitalContractStart,
  provisionDigitalContractSuccess,
  // POST DEPROVISION
  deprovisionDigitalContractFailure,
  deprovisionDigitalContractReset,
  deprovisionDigitalContractStart,
  deprovisionDigitalContractSuccess,
} from './digitalContract.actions';

import type {
  TPostDigitalContractSuccess,
  TGetAllDigitalContractsSuccess,
  TGetDigitalContractSuccess,
  TPatchActivateDigitalContractSuccess,
  TPatchAcceptDigitalContractSuccess,
  TPatchAssociateAzureSuccess,
  TGetProvisioningStatusSuccess,
  TProvisionDigitalContractSuccess,
  TDeprovisionDigitalContractSuccess
} from './digitalContract.typeDefs';

import { IDefaults } from '@redux/typedefs';

export interface IDigitalContractState {
  // GET ALL
  getAllDigitalContractsData: null | TGetAllDigitalContractsSuccess;
  getAllDigitalContractsError: IDefaults['errorMessage'];
  getAllDigitalContractsState: IDefaults['state'];

  // GET ONE
  getDigitalContractData: null | TGetDigitalContractSuccess;
  getDigitalContractError: IDefaults['errorMessage'];
  getDigitalContractState: IDefaults['state'];

  // PATCH ACTIVATE
  patchActivateDigitalContractData: null | TPatchActivateDigitalContractSuccess;
  patchActivateDigitalContractError: IDefaults['errorMessage'];
  patchActivateDigitalContractState: IDefaults['state'];

  // PATCH ACCEPT
  patchAcceptDigitalContractData: null | TPatchAcceptDigitalContractSuccess;
  patchAcceptDigitalContractError: IDefaults['errorMessage'];
  patchAcceptDigitalContractState: IDefaults['state'];

  // POST
  postDigitalContractData: null | TPostDigitalContractSuccess;
  postDigitalContractError: IDefaults['errorMessage'];
  postDigitalContractState: IDefaults['state'];

  // PATCH ASSOCIATE AZURE
  patchAssociateAzureData: null | TPatchAssociateAzureSuccess;
  patchAssociateAzureError: IDefaults['errorMessage'];
  patchAssociateAzureState: IDefaults['state'];

  // GET PROVISIONING STATUS
  getProvisioningStatusData: null | TPatchAssociateAzureSuccess;
  getProvisioningStatusError: IDefaults['errorMessage'];
  getProvisioningStatusState: IDefaults['state'];

  // POST PROVISION
  provisionDigitalContractData: null | TProvisionDigitalContractSuccess;
  provisionDigitalContractError: IDefaults['errorMessage'];
  provisionDigitalContractState: IDefaults['state'];

  // POST DEPROVISION
  deprovisionDigitalContractData: null | TDeprovisionDigitalContractSuccess;
  deprovisionDigitalContractError: IDefaults['errorMessage'];
  deprovisionDigitalContractState: IDefaults['state'];
}

const INITIAL_STATE: IDigitalContractState = {
  // GET ALL
  getAllDigitalContractsData: null,
  getAllDigitalContractsError: null,
  getAllDigitalContractsState: null,

  // GET ONE
  getDigitalContractData: null,
  getDigitalContractError: null,
  getDigitalContractState: null,

  // PATCH ACCEPT
  patchAcceptDigitalContractData: null,
  patchAcceptDigitalContractError: null,
  patchAcceptDigitalContractState: null,

  // PATCH ACTIVATE
  patchActivateDigitalContractData: null,
  patchActivateDigitalContractError: null,
  patchActivateDigitalContractState: null,

  // POST
  postDigitalContractData: null,
  postDigitalContractError: null,
  postDigitalContractState: null,

  // POST
  patchAssociateAzureData: null,
  patchAssociateAzureError: null,
  patchAssociateAzureState: null,

  // GET PROVISIONING STATUS
  getProvisioningStatusData: null,
  getProvisioningStatusError: null,
  getProvisioningStatusState: null,

  // POST PROVISION
  provisionDigitalContractData: null,
  provisionDigitalContractError: null,
  provisionDigitalContractState: null,

  // POST DEPROVISION
  deprovisionDigitalContractData: null,
  deprovisionDigitalContractError: null,
  deprovisionDigitalContractState: null,
};

// tslint:disable-next-line: no-unsafe-any tslint:disable-next-line: typedef
const digitalContractReducer = createReducer(INITIAL_STATE)
  // GET PROVISIONING STATUS

  .handleAction(
    getProvisioningStatusStart,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      getProvisioningStatusData: null,
      getProvisioningStatusError: null,
      getProvisioningStatusState: 'isLoading',
    })
  )
  .handleAction(
    getProvisioningStatusSuccess,
    (
      state: IDigitalContractState,
      action: { payload: TPostDigitalContractSuccess }
    ): IDigitalContractState => ({
      ...state,
      getProvisioningStatusData: action.payload,
      getProvisioningStatusError: null,
      getProvisioningStatusState: 'success',
    })
  )
  .handleAction(
    getProvisioningStatusFailure,
    (
      state: IDigitalContractState,
      action: { payload: IDefaults['errorMessage'] }
    ): IDigitalContractState => ({
      ...state,
      getProvisioningStatusData: null,
      getProvisioningStatusError: action.payload,
      getProvisioningStatusState: 'failure',
    })
  )
  .handleAction(
    getProvisioningStatusReset,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      getProvisioningStatusData: null,
      getProvisioningStatusError: null,
      getProvisioningStatusState: null,
    })
  )
  // PATCH ASSOCIATE AZURE

  .handleAction(
    patchAssociateAzureStart,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      patchAssociateAzureData: null,
      patchAssociateAzureError: null,
      patchAssociateAzureState: 'isLoading',
    })
  )
  .handleAction(
    patchAssociateAzureSuccess,
    (
      state: IDigitalContractState,
      action: { payload: TPostDigitalContractSuccess }
    ): IDigitalContractState => ({
      ...state,
      patchAssociateAzureData: action.payload,
      patchAssociateAzureError: null,
      patchAssociateAzureState: 'success',
    })
  )
  .handleAction(
    patchAssociateAzureFailure,
    (
      state: IDigitalContractState,
      action: { payload: IDefaults['errorMessage'] }
    ): IDigitalContractState => ({
      ...state,
      patchAssociateAzureData: null,
      patchAssociateAzureError: action.payload,
      patchAssociateAzureState: 'failure',
    })
  )
  .handleAction(
    patchAssociateAzureReset,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      patchAssociateAzureData: null,
      patchAssociateAzureError: null,
      patchAssociateAzureState: null,
    })
  )
  // POST

  .handleAction(
    postDigitalContractStart,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      postDigitalContractData: null,
      postDigitalContractError: null,
      postDigitalContractState: 'isLoading',
    })
  )
  .handleAction(
    postDigitalContractSuccess,
    (
      state: IDigitalContractState,
      action: { payload: TPostDigitalContractSuccess }
    ): IDigitalContractState => ({
      ...state,
      postDigitalContractData: action.payload,
      postDigitalContractError: null,
      postDigitalContractState: 'success',
    })
  )
  .handleAction(
    postDigitalContractFailure,
    (
      state: IDigitalContractState,
      action: { payload: IDefaults['errorMessage'] }
    ): IDigitalContractState => ({
      ...state,
      postDigitalContractData: null,
      postDigitalContractError: action.payload,
      postDigitalContractState: 'failure',
    })
  )
  .handleAction(
    postDigitalContractReset,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      postDigitalContractData: null,
      postDigitalContractError: null,
      postDigitalContractState: null,
    })
  )

  // GET ALL

  .handleAction(
    getAllDigitalContractsStart,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      getAllDigitalContractsData: null,
      getAllDigitalContractsError: null,
      getAllDigitalContractsState: 'isLoading',
    })
  )
  .handleAction(
    getAllDigitalContractsSuccess,
    (
      state: IDigitalContractState,
      action: { payload: TGetAllDigitalContractsSuccess }
    ): IDigitalContractState => ({
      ...state,
      getAllDigitalContractsData: action.payload,
      getAllDigitalContractsError: null,
      getAllDigitalContractsState: 'success',
    })
  )
  .handleAction(
    getAllDigitalContractsFailure,
    (
      state: IDigitalContractState,
      action: { payload: IDefaults['errorMessage'] }
    ): IDigitalContractState => ({
      ...state,
      getAllDigitalContractsData: null,
      getAllDigitalContractsError: action.payload,
      getAllDigitalContractsState: 'failure',
    })
  )
  .handleAction(
    getAllDigitalContractsReset,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      getAllDigitalContractsData: null,
      getAllDigitalContractsError: null,
      getAllDigitalContractsState: null,
    })
  )

  // GET ONE

  .handleAction(
    getDigitalContractStart,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      getDigitalContractData: null,
      getDigitalContractError: null,
      getDigitalContractState: 'isLoading',
    })
  )
  .handleAction(
    getDigitalContractSuccess,
    (
      state: IDigitalContractState,
      action: { payload: TGetDigitalContractSuccess }
    ): IDigitalContractState => ({
      ...state,
      getDigitalContractData: action.payload,
      getDigitalContractError: null,
      getDigitalContractState: 'success',
    })
  )
  .handleAction(
    getDigitalContractFailure,
    (
      state: IDigitalContractState,
      action: { payload: IDefaults['errorMessage'] }
    ): IDigitalContractState => ({
      ...state,
      getDigitalContractData: null,
      getDigitalContractError: action.payload,
      getDigitalContractState: 'failure',
    })
  )
  .handleAction(
    getDigitalContractReset,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      getDigitalContractData: null,
      getDigitalContractError: null,
      getDigitalContractState: null,
    })
  )

  // PATCH ACTIVATE

  .handleAction(
    patchActivateDigitalContractStart,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      patchActivateDigitalContractData: null,
      patchActivateDigitalContractError: null,
      patchActivateDigitalContractState: 'isLoading',
    })
  )
  .handleAction(
    patchActivateDigitalContractSuccess,
    (
      state: IDigitalContractState,
      action: { payload: TPatchActivateDigitalContractSuccess }
    ): IDigitalContractState => ({
      ...state,
      patchActivateDigitalContractData: action.payload,
      patchActivateDigitalContractError: null,
      patchActivateDigitalContractState: 'success',
    })
  )
  .handleAction(
    patchActivateDigitalContractFailure,
    (
      state: IDigitalContractState,
      action: { payload: IDefaults['errorMessage'] }
    ): IDigitalContractState => ({
      ...state,
      patchActivateDigitalContractData: null,
      patchActivateDigitalContractError: action.payload,
      patchActivateDigitalContractState: 'failure',
    })
  )
  .handleAction(
    patchActivateDigitalContractReset,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      patchActivateDigitalContractData: null,
      patchActivateDigitalContractError: null,
      patchActivateDigitalContractState: null,
    })
  )

  // PATCH ACTIVATE

  .handleAction(
    patchAcceptDigitalContractStart,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      patchAcceptDigitalContractData: null,
      patchAcceptDigitalContractError: null,
      patchAcceptDigitalContractState: 'isLoading',
    })
  )
  .handleAction(
    patchAcceptDigitalContractSuccess,
    (
      state: IDigitalContractState,
      action: { payload: TPatchAcceptDigitalContractSuccess }
    ): IDigitalContractState => ({
      ...state,
      patchAcceptDigitalContractData: action.payload,
      patchAcceptDigitalContractError: null,
      patchAcceptDigitalContractState: 'success',
    })
  )
  .handleAction(
    patchAcceptDigitalContractFailure,
    (
      state: IDigitalContractState,
      action: { payload: IDefaults['errorMessage'] }
    ): IDigitalContractState => ({
      ...state,
      patchAcceptDigitalContractData: null,
      patchAcceptDigitalContractError: action.payload,
      patchAcceptDigitalContractState: 'failure',
    })
  )
  .handleAction(
    patchAcceptDigitalContractReset,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      patchAcceptDigitalContractData: null,
      patchAcceptDigitalContractError: null,
      patchAcceptDigitalContractState: null,
    })
  )

  // POST PROVISION

  .handleAction(
    provisionDigitalContractStart,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      provisionDigitalContractData: null,
      provisionDigitalContractError: null,
      provisionDigitalContractState: 'isLoading',
    })
  )
  .handleAction(
    provisionDigitalContractSuccess,
    (
      state: IDigitalContractState,
      action: { payload: TProvisionDigitalContractSuccess }
    ): IDigitalContractState => ({
      ...state,
      provisionDigitalContractData: action.payload,
      provisionDigitalContractError: null,
      provisionDigitalContractState: 'success',
    })
  )
  .handleAction(
    provisionDigitalContractFailure,
    (
      state: IDigitalContractState,
      action: { payload: IDefaults['errorMessage'] }
    ): IDigitalContractState => ({
      ...state,
     provisionDigitalContractData: null,
     provisionDigitalContractError: action.payload,
     provisionDigitalContractState: 'failure',
    })
  )
  .handleAction(
    provisionDigitalContractReset,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      provisionDigitalContractData: null,
      provisionDigitalContractError: null,
      provisionDigitalContractState: null,
    })
  )

  // POST DEPROVISION

  .handleAction(
    deprovisionDigitalContractStart,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      deprovisionDigitalContractData: null,
      deprovisionDigitalContractError: null,
      deprovisionDigitalContractState: 'isLoading',
    })
  )
  .handleAction(
    deprovisionDigitalContractSuccess,
    (
      state: IDigitalContractState,
      action: { payload: TDeprovisionDigitalContractSuccess }
    ): IDigitalContractState => ({
      ...state,
      deprovisionDigitalContractData: action.payload,
      deprovisionDigitalContractError: null,
      deprovisionDigitalContractState: 'success',
    })
  )
  .handleAction(
    deprovisionDigitalContractFailure,
    (
      state: IDigitalContractState,
      action: { payload: IDefaults['errorMessage'] }
    ): IDigitalContractState => ({
      ...state,
      deprovisionDigitalContractData: null,
     deprovisionDigitalContractError: action.payload,
     deprovisionDigitalContractState: 'failure',
    })
  )
  .handleAction(
    deprovisionDigitalContractReset,
    (state: IDigitalContractState): IDigitalContractState => ({
      ...state,
      deprovisionDigitalContractData: null,
      deprovisionDigitalContractError: null,
      deprovisionDigitalContractState: null,
    })
  );

export default digitalContractReducer;
