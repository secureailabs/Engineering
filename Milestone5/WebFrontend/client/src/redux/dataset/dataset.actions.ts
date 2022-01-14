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
  | ActionType<typeof getDatasetReset>;

// POST REGISTER

export const postDatasetStart = createAction(
  // Type
  'Dataset/POST_DATASET_START',
  // Payload
  (data: TPostDatasetStart) => data
)();

export const postDatasetSuccess: EmptyActionCreator<string> = createAction(
  'Dataset/POST_DATASET_SUCCESS'
  // Payload
)();

export const postDatasetFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'Dataset/POST_DATASET_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const postDatasetReset: EmptyActionCreator<string> = createAction(
  'Dataset/POST_DATASET_RESET'
)();

// PATCH ACTIVATE

export const patchActivateDatasetStart = createAction(
  // Type
  'Dataset/PATCH_ACTIVATE_DATASET_START',
  // Payload
  (data: TPatchActivateDatasetStart) => data
)();

export const patchActivateDatasetSuccess: EmptyActionCreator<string> = createAction(
  'Dataset/PATCH_ACTIVATE_DATASET_SUCCESS'
  // Payload
)();

export const patchActivateDatasetFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'Dataset/PATCH_ACTIVATE_DATASET_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const patchActivateDatasetReset: EmptyActionCreator<string> = createAction(
  'Dataset/PATCH_ACTIVATE_DATASET_RESET'
)();

// PATCH ACCEPT

export const patchAcceptDatasetStart = createAction(
  // Type
  'Dataset/PATCH_ACCEPT_DATASET_START',
  // Payload
  (data: TPatchAcceptDatasetStart) => data
)();

export const patchAcceptDatasetSuccess: EmptyActionCreator<string> = createAction(
  'Dataset/PATCH_ACCEPT_DATASET_SUCCESS'
  // Payload
)();

export const patchAcceptDatasetFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'Dataset/PATCH_ACCEPT_DATASET_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const patchAcceptDatasetReset: EmptyActionCreator<string> = createAction(
  'Dataset/PATCH_ACCEPT_DATASET_RESET'
)();

// GET ALL

export const getAllDatasetsStart = createAction(
  // Type
  'Dataset/GET_ALL_DATASETS_START'
)();
export const getAllDatasetsSuccess: (
  data: TGetAllDatasetsSuccess
) => PayloadAction<string, TGetAllDatasetsSuccess> = createAction(
  'Dataset/GET_ALL_DATASETS_SUCCESS',
  // Payload
  (data: TGetAllDatasetsSuccess) => data
)();
export const getAllDatasetsFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'Dataset/GET_ALL_DATASETS_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getAllDatasetsReset: EmptyActionCreator<string> = createAction(
  'Dataset/GET_ALL_DATASETS_RESET'
)();

// GET ONE

export const getDatasetStart = createAction(
  // Type
  'Dataset/GET_DATASET_START',
  // Payload
  (data: TGetDatasetStart) => data
)();
export const getDatasetSuccess: (
  data: TGetDatasetSuccess
) => PayloadAction<string, TGetDatasetSuccess> = createAction(
  'Dataset/GET_DATASET_SUCCESS',
  // Payload
  (data: TGetDatasetSuccess) => data
)();
export const getDatasetFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'Dataset/GET_DATASET_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getDatasetReset: EmptyActionCreator<string> = createAction(
  'Dataset/GET_DATASET_RESET'
)();
