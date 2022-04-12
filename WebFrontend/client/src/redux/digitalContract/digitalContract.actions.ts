import {
  ActionType,
  createAction,
  EmptyActionCreator,
  PayloadAction,
} from 'typesafe-actions';

import type { IDefaults } from '@redux/typedefs';

import type {
  TPostDigitalContractStart,
  TPostDigitalContractSuccess,
  TPatchAcceptDigitalContractStart,
  TPatchAcceptDigitalContractSuccess,
  TPatchActivateDigitalContractStart,
  TPatchActivateDigitalContractSuccess,
  TGetAllDigitalContractsSuccess,
  TGetDigitalContractSuccess,
  TGetDigitalContractStart,
  TPatchAssociateAzureStart,
  TGetProvisioningStatusStart,
  TGetProvisioningStatusSuccess,
  TProvisionDigitalContractStart,
  TDeprovisionDigitalContractStart,
} from './digitalContract.typeDefs';

export type digitalContractActions =
  // PATCH  ASSOCIATE WITH AZURE TEMPLATE
  | ActionType<typeof patchAssociateAzureStart>
  | ActionType<typeof patchAssociateAzureSuccess>
  | ActionType<typeof patchAssociateAzureFailure>
  | ActionType<typeof patchAssociateAzureReset>
  // POST
  | ActionType<typeof postDigitalContractStart>
  | ActionType<typeof postDigitalContractSuccess>
  | ActionType<typeof postDigitalContractFailure>
  | ActionType<typeof postDigitalContractReset>
  // PATCH ACTIVATE
  | ActionType<typeof patchActivateDigitalContractStart>
  | ActionType<typeof patchActivateDigitalContractSuccess>
  | ActionType<typeof patchActivateDigitalContractFailure>
  | ActionType<typeof patchActivateDigitalContractReset>
  // PATCH ACCEPT
  | ActionType<typeof patchAcceptDigitalContractStart>
  | ActionType<typeof patchAcceptDigitalContractSuccess>
  | ActionType<typeof patchAcceptDigitalContractFailure>
  | ActionType<typeof patchAcceptDigitalContractReset>
  // GET ALL
  | ActionType<typeof getAllDigitalContractsStart>
  | ActionType<typeof getAllDigitalContractsSuccess>
  | ActionType<typeof getAllDigitalContractsFailure>
  | ActionType<typeof getAllDigitalContractsReset>
  // GET
  | ActionType<typeof getDigitalContractStart>
  | ActionType<typeof getDigitalContractSuccess>
  | ActionType<typeof getDigitalContractFailure>
  | ActionType<typeof getDigitalContractReset>

  // GET
  | ActionType<typeof getDigitalContractStart>
  | ActionType<typeof getDigitalContractSuccess>
  | ActionType<typeof getDigitalContractFailure>
  | ActionType<typeof getDigitalContractReset>

  // POST Provision
  | ActionType<typeof provisionDigitalContractStart>
  | ActionType<typeof provisionDigitalContractSuccess>
  | ActionType<typeof provisionDigitalContractFailure>
  | ActionType<typeof provisionDigitalContractReset>

  // POST Deprovision
  | ActionType<typeof deprovisionDigitalContractStart>
  | ActionType<typeof deprovisionDigitalContractSuccess>
  | ActionType<typeof deprovisionDigitalContractFailure>
  | ActionType<typeof deprovisionDigitalContractReset>;

// PATCH  ASSOCIATE WITH AZURE TEMPLATE

export const patchAssociateAzureStart = createAction(
  // Type
  'digitalContract/PATCH_ASSOCIATE_AZURE_START',
  // Payload
  (data: TPatchAssociateAzureStart) => data
)();

export const patchAssociateAzureSuccess: EmptyActionCreator<string> = createAction(
  'digitalContract/PATCH_ASSOCIATE_AZURE_SUCCESS'
  // Payload
)();

export const patchAssociateAzureFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'digitalContract/PATCH_ASSOCIATE_AZURE_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const patchAssociateAzureReset: EmptyActionCreator<string> = createAction(
  'digitalContract/PATCH_ASSOCIATE_AZURE_RESET'
)();

// POST REGISTER

export const postDigitalContractStart = createAction(
  // Type
  'digitalContract/POST_DIGITAL_CONTRACT_START',
  // Payload
  (data: TPostDigitalContractStart) => data
)();

export const postDigitalContractSuccess: EmptyActionCreator<string> = createAction(
  'digitalContract/POST_DIGITAL_CONTRACT_SUCCESS'
  // Payload
)();

export const postDigitalContractFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'digitalContract/POST_DIGITAL_CONTRACT_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const postDigitalContractReset: EmptyActionCreator<string> = createAction(
  'digitalContract/POST_DIGITAL_CONTRACT_RESET'
)();

// PATCH ACTIVATE

export const patchActivateDigitalContractStart = createAction(
  // Type
  'digitalContract/PATCH_ACTIVATE_DIGITAL_CONTRACT_START',
  // Payload
  (data: TPatchActivateDigitalContractStart) => data
)();

export const patchActivateDigitalContractSuccess: EmptyActionCreator<string> = createAction(
  'digitalContract/PATCH_ACTIVATE_DIGITAL_CONTRACT_SUCCESS'
  // Payload
)();

export const patchActivateDigitalContractFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'digitalContract/PATCH_ACTIVATE_DIGITAL_CONTRACT_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const patchActivateDigitalContractReset: EmptyActionCreator<string> = createAction(
  'digitalContract/PATCH_ACTIVATE_DIGITAL_CONTRACT_RESET'
)();

// PATCH ACCEPT

export const patchAcceptDigitalContractStart = createAction(
  // Type
  'digitalContract/PATCH_ACCEPT_DIGITAL_CONTRACT_START',
  // Payload
  (data: TPatchAcceptDigitalContractStart) => data
)();

export const patchAcceptDigitalContractSuccess: EmptyActionCreator<string> = createAction(
  'digitalContract/PATCH_ACCEPT_DIGITAL_CONTRACT_SUCCESS'
  // Payload
)();

export const patchAcceptDigitalContractFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'digitalContract/PATCH_ACCEPT_DIGITAL_CONTRACT_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const patchAcceptDigitalContractReset: EmptyActionCreator<string> = createAction(
  'digitalContract/PATCH_ACCEPT_DIGITAL_CONTRACT_RESET'
)();

// GET ALL

export const getAllDigitalContractsStart = createAction(
  // Type
  'digitalContract/GET_ALL_DIGITAL_CONTRACTS_START'
)();
export const getAllDigitalContractsSuccess: (
  data: TGetAllDigitalContractsSuccess
) => PayloadAction<string, TGetAllDigitalContractsSuccess> = createAction(
  'digitalContract/GET_ALL_DIGITAL_CONTRACTS_SUCCESS',
  // Payload
  (data: TGetAllDigitalContractsSuccess) => data
)();
export const getAllDigitalContractsFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'digitalContract/GET_ALL_DIGITAL_CONTRACTS_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getAllDigitalContractsReset: EmptyActionCreator<string> = createAction(
  'digitalContract/GET_ALL_DIGITAL_CONTRACTS_RESET'
)();

// GET ONE

export const getDigitalContractStart = createAction(
  // Type
  'digitalContract/GET_DIGITAL_CONTRACT_START',
  // Payload
  (data: TGetDigitalContractStart) => data
)();
export const getDigitalContractSuccess: (
  data: TGetDigitalContractSuccess
) => PayloadAction<string, TGetDigitalContractSuccess> = createAction(
  'digitalContract/GET_DIGITAL_CONTRACT_SUCCESS',
  // Payload
  (data: TGetDigitalContractSuccess) => data
)();
export const getDigitalContractFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'digitalContract/GET_DIGITAL_CONTRACT_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getDigitalContractReset: EmptyActionCreator<string> = createAction(
  'digitalContract/GET_DIGITAL_CONTRACT_RESET'
)();

// GET PROVISIONING STATUS

export const getProvisioningStatusStart = createAction(
  // Type
  'digitalContract/GET_PROVISIONING_STATUS_START',
  // Payload
  (data: TGetProvisioningStatusStart) => data
)();
export const getProvisioningStatusSuccess: (
  data: TGetProvisioningStatusSuccess
) => PayloadAction<string, TGetProvisioningStatusSuccess> = createAction(
  'digitalContract/GET_PROVISIONING_STATUS_SUCCESS',
  // Payload
  (data: TGetProvisioningStatusSuccess) => data
)();
export const getProvisioningStatusFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'digitalContract/GET_PROVISIONING_STATUS_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getProvisioningStatusReset: EmptyActionCreator<string> = createAction(
  'digitalContract/GET_PROVISIONING_STATUS_RESET'
)();

// POST PROVISION

export const provisionDigitalContractStart = createAction(
  // Type
  'digitalContract/PROVISION_DIGITAL_CONTRACT_START',
  // Payload
  (data: TProvisionDigitalContractStart) => data
)();

export const provisionDigitalContractSuccess: EmptyActionCreator<string> = createAction(
  'digitalContract/PROVISION_DIGITAL_CONTRACT_SUCCESS'
  // Payload
)();

export const provisionDigitalContractFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'digitalContract/PROVISION_DIGITAL_CONTRACT_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const provisionDigitalContractReset: EmptyActionCreator<string> = createAction(
  'digitalContract/PROVISION_DIGITAL_CONTRACT_RESET'
)();


// POST DEPROVISION

export const deprovisionDigitalContractStart = createAction(
  // Type
  'digitalContract/DEPROVISION_DIGITAL_CONTRACT_START',
  // Payload
  (data: TDeprovisionDigitalContractStart) => data
)();

export const deprovisionDigitalContractSuccess: EmptyActionCreator<string> = createAction(
  'digitalContract/DEPROVISION_DIGITAL_CONTRACT_SUCCESS'
  // Payload
)();

export const deprovisionDigitalContractFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'digitalContract/DEPROVISION_DIGITAL_CONTRACT_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const deprovisionDigitalContractReset: EmptyActionCreator<string> = createAction(
  'digitalContract/DEPROVISION_DIGITAL_CONTRACT_RESET'
)();