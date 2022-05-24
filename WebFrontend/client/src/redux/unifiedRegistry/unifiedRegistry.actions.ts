import {
  ActionType,
  createAction,
  EmptyActionCreator,
  PayloadAction,
} from 'typesafe-actions';

import type { IDefaults } from '@app/redux/typedefs';

import type {
  TPostUnifiedRegistryStart,
  TPostUnifiedRegistrySuccess,
  TPutUnifiedRegistryStart,
  TGetAllUnifiedRegistriesSuccess,
  TGetUnifiedRegistrySuccess,
  TGetUnifiedRegistryStart,
  TDeleteUnifiedRegistryStart,
  TDeleteUnifiedRegistrySuccess,
} from './unifiedRegistry.types';

export type unifiedRegistryActions =
  // POST
  | ActionType<typeof postUnifiedRegistryStart>
  | ActionType<typeof postUnifiedRegistrySuccess>
  | ActionType<typeof postUnifiedRegistryFailure>
  | ActionType<typeof postUnifiedRegistryReset>
  // PUT ACTIVATE
  | ActionType<typeof putUnifiedRegistryStart>
  | ActionType<typeof putUnifiedRegistrySuccess>
  | ActionType<typeof putUnifiedRegistryFailure>
  | ActionType<typeof putUnifiedRegistryReset>
  // GET ALL
  | ActionType<typeof getAllUnifiedRegistriesStart>
  | ActionType<typeof getAllUnifiedRegistriesSuccess>
  | ActionType<typeof getAllUnifiedRegistriesFailure>
  | ActionType<typeof getAllUnifiedRegistriesReset>
  // GET
  | ActionType<typeof getUnifiedRegistryStart>
  | ActionType<typeof getUnifiedRegistrySuccess>
  | ActionType<typeof getUnifiedRegistryFailure>
  | ActionType<typeof getUnifiedRegistryReset>
  // GET
  | ActionType<typeof deleteUnifiedRegistryStart>
  | ActionType<typeof deleteUnifiedRegistrySuccess>
  | ActionType<typeof deleteUnifiedRegistryFailure>
  | ActionType<typeof deleteUnifiedRegistryReset>;

// POST REGISTER

export const postUnifiedRegistryStart = createAction(
  'unifiedRegistry/POST_UNIFIED_REGISTRY_START',
  (data: TPostUnifiedRegistryStart) => data
)();
export const postUnifiedRegistrySuccess: EmptyActionCreator<string> = createAction(
  'unifiedRegistry/POST_UNIFIED_REGISTRY_SUCCESS'
)();
export const postUnifiedRegistryFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'unifiedRegistry/POST_UNIFIED_REGISTRY_FAILURE',
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const postUnifiedRegistryReset: EmptyActionCreator<string> = createAction(
  'unifiedRegistry/POST_UNIFIED_REGISTRY_RESET'
)();

// PUT
export const putUnifiedRegistryStart = createAction(
  'unifiedRegistry/PUT_UNIFIED_REGISTRY_START',
  (data: TPutUnifiedRegistryStart) => data
)();
export const putUnifiedRegistrySuccess: EmptyActionCreator<string> = createAction(
  'unifiedRegistry/PUT_UNIFIED_REGISTRY_SUCCESS'
)();
export const putUnifiedRegistryFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'unifiedRegistry/PUT_UNIFIED_REGISTRY_FAILURE',
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const putUnifiedRegistryReset: EmptyActionCreator<string> = createAction(
  'unifiedRegistry/PUT_UNIFIED_REGISTRY_RESET'
)();

// GET ALL
export const getAllUnifiedRegistriesStart = createAction(
  'unifiedRegistry/GET_ALL_UNIFIED_REGISTRIES_START'
)();
export const getAllUnifiedRegistriesSuccess: (
  data: TGetAllUnifiedRegistriesSuccess
) => PayloadAction<string, TGetAllUnifiedRegistriesSuccess> = createAction(
  'unifiedRegistry/GET_ALL_UNIFIED_REGISTRIES_SUCCESS',
  (data: TGetAllUnifiedRegistriesSuccess) => data
)();
export const getAllUnifiedRegistriesFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'unifiedRegistry/GET_ALL_UNIFIED_REGISTRIES_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getAllUnifiedRegistriesReset: EmptyActionCreator<string> = createAction(
  'unifiedRegistry/GET_ALL_UNIFIED_REGISTRIES_RESET'
)();

// GET ONE
export const getUnifiedRegistryStart = createAction(
  'unifiedRegistry/GET_UNIFIED_REGISTRY_START',
  (data: TGetUnifiedRegistryStart) => data
)();
export const getUnifiedRegistrySuccess: (
  data: TGetUnifiedRegistrySuccess
) => PayloadAction<string, TGetUnifiedRegistrySuccess> = createAction(
  'unifiedRegistry/GET_UNIFIED_REGISTRY_SUCCESS',
  (data: TGetUnifiedRegistrySuccess) => data
)();
export const getUnifiedRegistryFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'unifiedRegistry/GET_UNIFIED_REGISTRY_FAILURE',
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getUnifiedRegistryReset: EmptyActionCreator<string> = createAction(
  'unifiedRegistry/GET_UNIFIED_REGISTRY_RESET'
)();

// DELETE
export const deleteUnifiedRegistryStart = createAction(
  'unifiedRegistry/DELETE_UNIFIED_REGISTRY_START',
  (data: TDeleteUnifiedRegistryStart) => data
)();
//@ts-ignore
export const deleteUnifiedRegistrySuccess: (
  data: TDeleteUnifiedRegistryStart
) => PayloadAction<string, TDeleteUnifiedRegistrySuccess> = createAction(
  'unifiedRegistry/DELETE_UNIFIED_REGISTRY_SUCCESS',
  (data: TDeleteUnifiedRegistryStart) => data
)();
export const deleteUnifiedRegistryFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'unifiedRegistry/DELETE_UNIFIED_REGISTRY_FAILURE',
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const deleteUnifiedRegistryReset: EmptyActionCreator<string> = createAction(
  'unifiedRegistry/DELETE_UNIFIED_REGISTRY_RESET'
)();
