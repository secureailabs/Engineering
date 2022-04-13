import {
  ActionType,
  createAction,
  EmptyActionCreator,
  PayloadAction,
} from 'typesafe-actions';

import type { IDefaults } from '@redux/typedefs';

import type {
  TPostAzureTemplateStart,
  TGetAllAzureTemplatesSuccess,
  TGetAzureTemplateStart,
  TPutUpdateAzureSecretStart,
  TGetAzureTemplateSuccess,
  TPutUpdateAzureTemplateStart,
  TDeleteAzureTemplateStart,
} from './azureTemplate.typesDefs';

export type AzureTemplateActions =
  // POST POST TEMPLATE
  | ActionType<typeof postAzureTemplateStart>
  | ActionType<typeof postAzureTemplateSuccess>
  | ActionType<typeof postAzureTemplateFailure>
  | ActionType<typeof postAzureTemplateReset>
  // GET GET_ALL TEMPLATES
  | ActionType<typeof getAllAzureTemplatesStart>
  | ActionType<typeof getAllAzureTemplatesSuccess>
  | ActionType<typeof getAllAzureTemplatesFailure>
  | ActionType<typeof getAllAzureTemplatesReset>
  // GET AZURE TEMPLATE
  | ActionType<typeof getAzureTemplateStart>
  | ActionType<typeof getAzureTemplateSuccess>
  | ActionType<typeof getAzureTemplateFailure>
  | ActionType<typeof getAzureTemplateReset>

  // PUT UPDATE TEMPLATE
  | ActionType<typeof putUpdateAzureTemplateStart>
  | ActionType<typeof putUpdateAzureTemplateSuccess>
  | ActionType<typeof putUpdateAzureTemplateFailure>
  | ActionType<typeof putUpdateAzureTemplateReset>
  // PUT UPDATE SECRET
  | ActionType<typeof putUpdateAzureSecretStart>
  | ActionType<typeof putUpdateAzureSecretSuccess>
  | ActionType<typeof putUpdateAzureSecretFailure>
  | ActionType<typeof putUpdateAzureSecretReset>
  // DELETE
  | ActionType<typeof deleteAzureTemplateStart>
  | ActionType<typeof deleteAzureTemplateSuccess>
  | ActionType<typeof deleteAzureTemplateFailure>
  | ActionType<typeof deleteAzureTemplateReset>;

export const postAzureTemplateStart = createAction(
  'AzureTemplateManager/POST_AZURE_TEMPLATE_START',
  (data: TPostAzureTemplateStart) => data
)();
export const postAzureTemplateSuccess: EmptyActionCreator<string> = createAction(
  'AzureTemplateManager/POST_AZURE_TEMPLATE_SUCCESS'
)();
export const postAzureTemplateFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'AzureTemplateManager/POST_AZURE_TEMPLATE_FAILURE',
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const postAzureTemplateReset: EmptyActionCreator<string> = createAction(
  'AzureTemplateManager/POST_AZURE_TEMPLATE_RESET'
)();

// GET ALL TEMPLATES

export const getAllAzureTemplatesStart = createAction(
  'AzureTemplateManager/GET_ALL_AZURE_TEMPLATES_START'
)();
export const getAllAzureTemplatesSuccess: (
  data: TGetAllAzureTemplatesSuccess
) => PayloadAction<string, TGetAllAzureTemplatesSuccess> = createAction(
  'AzureTemplatesManager/GET_ALL_AZURE_TEMPLATES_SUCCESS',
  (data: TGetAllAzureTemplatesSuccess) => data
)();
export const getAllAzureTemplatesFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'AzureTemplatesManager/GET_ALL_AZURE_TEMPLATES_FAILURE',
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getAllAzureTemplatesReset: EmptyActionCreator<string> = createAction(
  'AzureTemplatesManager/GET_ALL_AZURE_TEMPLATES_RESET'
)();

// GET TEMPLATE

export const getAzureTemplateStart = createAction(
  'AzureTemplateManager/GET_AZURE_TEMPLATE_START',
  (data: TGetAzureTemplateStart) => data
)();
export const getAzureTemplateSuccess: (
  data: TGetAzureTemplateSuccess
) => PayloadAction<string, TGetAzureTemplateSuccess> = createAction(
  'AzureTemplatesManager/GET_AZURE_TEMPLATE_SUCCESS',
  (data: TGetAzureTemplateSuccess) => data
)();
export const getAzureTemplateFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'AzureTemplatesManager/GET_AZURE_TEMPLATE_FAILURE',
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getAzureTemplateReset: EmptyActionCreator<string> = createAction(
  'AzureTemplatesManager/GET_AZURE_TEMPLATE_RESET'
)();

// PUT UPDATE AZURE TEMPLATE

export const putUpdateAzureTemplateStart = createAction(
  'AzureTemplatesManager/PUT_UPDATE_AZURE_TEMPLATE_START',
  (data: TPutUpdateAzureTemplateStart) => data
)();
export const putUpdateAzureTemplateSuccess: EmptyActionCreator<string> = createAction(
  'AzureTemplatesManager/PUT_UPDATE_AZURE_TEMPLATE_SUCCESS'
)();
export const putUpdateAzureTemplateFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'AzureTemplatesManager/PUT_UPDATE_AZURE_TEMPLATE_FAILURE',
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const putUpdateAzureTemplateReset: EmptyActionCreator<string> = createAction(
  'AzureTemplatesManager/PUT_UPDATE_AZURE_TEMPLATE_RESET'
)();

// PUT UPDATE AZURE SECRET

export const putUpdateAzureSecretStart = createAction(
  'AzureTemplatesManager/PUT_UPDATE_AZURE_SECRET_START',
  (data: TPutUpdateAzureSecretStart) => data
)();
export const putUpdateAzureSecretSuccess: EmptyActionCreator<string> = createAction(
  'AzureTemplatesManager/PUT_UPDATE_AZURE_SECRET_SUCCESS'
)();
export const putUpdateAzureSecretFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'AzureTemplatesManager/PUT_UPDATE_AZURE_SECRET_FAILURE',
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const putUpdateAzureSecretReset: EmptyActionCreator<string> = createAction(
  'AzureTemplatesManager/PUT_UPDATE_AZURE_SECRET_RESET'
)();

// DELETE

export const deleteAzureTemplateStart = createAction(
  'AzureTemplatesManager/DELETE_AZURE_TEMPLATE_START',
  (data: TDeleteAzureTemplateStart) => data
)();
export const deleteAzureTemplateSuccess: EmptyActionCreator<string> = createAction(
  'AzureTemplatesManager/DELETE_AZURE_TEMPLATE_SUCCESS'
)();
export const deleteAzureTemplateFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'AzureTemplatesManager/DELETE_AZURE_TEMPLATE_FAILURE',
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const deleteAzureTemplateReset: EmptyActionCreator<string> = createAction(
  'AzureTemplatesManager/DELETE_AZURE_TEMPLATE_RESET'
)();
