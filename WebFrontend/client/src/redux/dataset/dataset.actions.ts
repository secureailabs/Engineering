import {
  ActionType,
  createAction,
  EmptyActionCreator,
  PayloadAction,
} from 'typesafe-actions';

import type { IDefaults } from '@redux/typedefs';

import type {
  TPostDatasetStart,
  TPostDatasetSuccess,
  TPatchAcceptDatasetStart,
  TPatchAcceptDatasetSuccess,
  TPatchActivateDatasetStart,
  TPatchActivateDatasetSuccess,
  TGetAllDatasetsSuccess,
  TGetDatasetSuccess,
  TGetDatasetStart,
  TGetDatasetVersionSuccess,
  TGetDatasetVersionStart,
} from './dataset.typeDefs';

export type datasetActions =
  // POST
  | ActionType<typeof postDatasetStart>
  | ActionType<typeof postDatasetSuccess>
  | ActionType<typeof postDatasetFailure>
  | ActionType<typeof postDatasetReset>
  // PATCH ACTIVATE
  | ActionType<typeof patchActivateDatasetStart>
  | ActionType<typeof patchActivateDatasetSuccess>
  | ActionType<typeof patchActivateDatasetFailure>
  | ActionType<typeof patchActivateDatasetReset>
  // PATCH ACCEPT
  | ActionType<typeof patchAcceptDatasetStart>
  | ActionType<typeof patchAcceptDatasetSuccess>
  | ActionType<typeof patchAcceptDatasetFailure>
  | ActionType<typeof patchAcceptDatasetReset>
  // GET ALL
  | ActionType<typeof getAllDatasetsStart>
  | ActionType<typeof getAllDatasetsSuccess>
  | ActionType<typeof getAllDatasetsFailure>
  | ActionType<typeof getAllDatasetsReset>
  // GET
  | ActionType<typeof getDatasetStart>
  | ActionType<typeof getDatasetSuccess>
  | ActionType<typeof getDatasetFailure>
  | ActionType<typeof getDatasetReset>
  // GET VERSION
  | ActionType<typeof getDatasetVersionStart>
  | ActionType<typeof getDatasetVersionSuccess>
  | ActionType<typeof getDatasetVersionFailure>
  | ActionType<typeof getDatasetVersionReset>;

// POST REGISTER

export const postDatasetStart = createAction(
  // Type
  'dataset/POST_DATASET_START',
  // Payload
  (data: TPostDatasetStart) => data
)();

export const postDatasetSuccess: EmptyActionCreator<string> = createAction(
  'dataset/POST_DATASET_SUCCESS'
  // Payload
)();

export const postDatasetFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'dataset/POST_DATASET_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const postDatasetReset: EmptyActionCreator<string> = createAction(
  'dataset/POST_DATASET_RESET'
)();

// PATCH ACTIVATE

export const patchActivateDatasetStart = createAction(
  // Type
  'dataset/PATCH_ACTIVATE_DATASET_START',
  // Payload
  (data: TPatchActivateDatasetStart) => data
)();

export const patchActivateDatasetSuccess: EmptyActionCreator<string> = createAction(
  'dataset/PATCH_ACTIVATE_DATASET_SUCCESS'
  // Payload
)();

export const patchActivateDatasetFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'dataset/PATCH_ACTIVATE_DATASET_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const patchActivateDatasetReset: EmptyActionCreator<string> = createAction(
  'dataset/PATCH_ACTIVATE_DATASET_RESET'
)();

// PATCH ACCEPT

export const patchAcceptDatasetStart = createAction(
  // Type
  'dataset/PATCH_ACCEPT_DATASET_START',
  // Payload
  (data: TPatchAcceptDatasetStart) => data
)();

export const patchAcceptDatasetSuccess: EmptyActionCreator<string> = createAction(
  'dataset/PATCH_ACCEPT_DATASET_SUCCESS'
  // Payload
)();

export const patchAcceptDatasetFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'dataset/PATCH_ACCEPT_DATASET_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const patchAcceptDatasetReset: EmptyActionCreator<string> = createAction(
  'dataset/PATCH_ACCEPT_DATASET_RESET'
)();

// GET ALL

export const getAllDatasetsStart = createAction(
  // Type
  'dataset/GET_ALL_DATASETS_START'
)();
export const getAllDatasetsSuccess: (
  data: TGetAllDatasetsSuccess
) => PayloadAction<string, TGetAllDatasetsSuccess> = createAction(
  'dataset/GET_ALL_DATASETS_SUCCESS',
  // Payload
  (data: TGetAllDatasetsSuccess) => data
)();
export const getAllDatasetsFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'dataset/GET_ALL_DATASETS_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getAllDatasetsReset: EmptyActionCreator<string> = createAction(
  'dataset/GET_ALL_DATASETS_RESET'
)();

// GET ONE

export const getDatasetStart = createAction(
  // Type
  'dataset/GET_DATASET_START',
  // Payload
  (data: TGetDatasetStart) => data
)();
export const getDatasetSuccess: (
  data: TGetDatasetSuccess
) => PayloadAction<string, TGetDatasetSuccess> = createAction(
  'dataset/GET_DATASET_SUCCESS',
  // Payload
  (data: TGetDatasetSuccess) => data
)();
export const getDatasetFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'dataset/GET_DATASET_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getDatasetReset: EmptyActionCreator<string> = createAction(
  'dataset/GET_DATASET_RESET'
)();

// GET ONE

export const getDatasetVersionStart = createAction(
  // Type
  'dataset/GET_DATASET_VERSION_START',
  // Payload
  (data: TGetDatasetVersionStart) => data
)();
export const getDatasetVersionSuccess: (
  data: TGetDatasetVersionSuccess
) => PayloadAction<string, TGetDatasetVersionSuccess> = createAction(
  'dataset/GET_DATASET_VERSION_SUCCESS',
  // Payload
  (data: TGetDatasetVersionSuccess) => data
)();
export const getDatasetVersionFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'dataset/GET_DATASET_VERSION_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getDatasetVersionReset: EmptyActionCreator<string> = createAction(
  'dataset/GET_DATASET_VERSION_RESET'
)();
