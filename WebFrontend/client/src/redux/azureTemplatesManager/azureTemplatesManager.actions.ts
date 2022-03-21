import {
    ActionType,
    createAction,
    EmptyActionCreator,
    PayloadAction,
  } from 'typesafe-actions';

import type { IDefaults } from '@redux/typedefs';

import type {
    TRegisterAzureTemplateStart,
    TRegisterAzureTemplateSuccess,
    TListAzureTemplatesStart,
    TListAzureTemplatesSuccess,
    TPullAzureTemplateStart,
    TPullAzureTemplateSuccess,
    TUpdateAzureTemplateStart,
    TDeleteAzureTemplateStart,
} from './azureTemplatesManager.typesDefs'

export type AzureTemplatesManagerActions =
// POST REGISTER TEMPLATE
| ActionType<typeof registerAzureTemplateStart>
| ActionType<typeof registerAzureTemplateSuccess>
| ActionType<typeof registerAzureTemplateFailure>
| ActionType<typeof registerAzureTemplateReset>
// GET LIST TEMPLATES
| ActionType<typeof listAzureTemplatesStart>
| ActionType<typeof listAzureTemplatesSuccess>
| ActionType<typeof listAzureTemplatesFailure>
| ActionType<typeof listAzureTemplatesReset>
// GET PULL TEMPLATE
| ActionType<typeof pullAzureTemplateStart>
| ActionType<typeof pullAzureTemplateSuccess>
| ActionType<typeof pullAzureTemplateFailure>
| ActionType<typeof pullAzureTemplateReset>
// PUT UPDATE TEMPLATE
| ActionType<typeof updateAzureTemplateStart>
| ActionType<typeof updateAzureTemplateSuccess>
| ActionType<typeof updateAzureTemplateFailure>
| ActionType<typeof updateAzureTemplateReset>
// PUT UPDATE SECRET
| ActionType<typeof updateAzureSecretStart>
| ActionType<typeof updateAzureSecretSuccess>
| ActionType<typeof updateAzureSecretFailure>
| ActionType<typeof updateAzureSecretReset>
// DELETE
| ActionType<typeof deleteAzureTemplateStart>
| ActionType<typeof deleteAzureTemplateSuccess>
| ActionType<typeof deleteAzureTemplateFailure>
| ActionType<typeof deleteAzureTemplateReset>

export const registerAzureTemplateStart = createAction(
    // Type
    'AzureTemplateManager/REGISTER_AZURE_TEMPLATE_START',
    // Payload
    (data: TRegisterAzureTemplateStart) => data
  )();
  
  export const registerAzureTemplateSuccess: EmptyActionCreator<string> = createAction(
    'AzureTemplateManager/REGISTER_AZURE_TEMPLATE_SUCCESS'
    // Payload
  )();
  
  export const registerAzureTemplateFailure: (
    error: IDefaults['errorMessage']
  ) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
    'AzureTemplateManager/REGISTER_AZURE_TEMPLATE_FAILURE',
    // Payload
    (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
  )();
  export const registerAzureTemplateReset: EmptyActionCreator<string> = createAction(
    'AzureTemplateManager/REGISTER_AZURE_TEMPLATE_RESET'
  )();

// GET LIST TEMPLATES

export const listAzureTemplatesStart = createAction(
    // Type
    'AzureTemplateManager/LIST_AZURE_TEMPLATES_START',
  )();
  export const listAzureTemplatesSuccess: (
    data: TListAzureTemplatesSuccess
  ) => PayloadAction<string, TListAzureTemplatesSuccess> = createAction(
    'AzureTemplatesManager/LIST_AZURE_TEMPLATES_SUCCESS',
    // Payload
    (data: TListAzureTemplatesSuccess) => data
  )();
  export const listAzureTemplatesFailure: (
    error: IDefaults['errorMessage']
  ) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
    'AzureTemplatesManager/LIST_AZURE_TEMPLATES_FAILURE',
    // Payload
    (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
  )();
  export const listAzureTemplatesReset: EmptyActionCreator<string> = createAction(
    'AzureTemplatesManager/LIST_AZURE_TEMPLATES_RESET'
  )();

  // GET PULL TEMPLATE
  
  export const pullAzureTemplateStart = createAction(
    // Type
    'AzureTemplatesManager/PULL_AZURE_TEMPLATE_START',
    // Payload
    (data: TPullAzureTemplateStart) => data
  )();
  export const pullAzureTemplateSuccess: (
    data: TPullAzureTemplateSuccess
  ) => PayloadAction<string, TPullAzureTemplateSuccess> = createAction(
    'AzureTemplatesManager/PULL_AZURE_TEMPLATE_SUCCESS',
    // Payload
    (data: TPullAzureTemplateSuccess) => data
  )();
  export const pullAzureTemplateFailure: (
    error: IDefaults['errorMessage']
  ) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
    'AzureTemplatesManager/PULL_AZURE_TEMPLATE_FAILURE',
    // Payload
    (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
  )();
  export const pullAzureTemplateReset: EmptyActionCreator<string> = createAction(
    'AzureTemplatesManager/PULL_AZURE_TEMPLATE_RESET',
  )();

// PUT UPDATE AZURE TEMPLATE

export const updateAzureTemplateStart = createAction(
  // Type
  'AzureTemplatesManager/UPDATE_AZURE_TEMPLATE_START',
  // Payload
  (data: TUpdateAzureTemplateStart) => data
)();

export const updateAzureTemplateSuccess: EmptyActionCreator<string> = createAction(
  'AzureTemplatesManager/UPDATE_AZURE_TEMPLATE_SUCCESS'
  // Payload
)();

export const updateAzureTemplateFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'AzureTemplatesManager/UPDATE_AZURE_TEMPLATE_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const updateAzureTemplateReset: EmptyActionCreator<string> = createAction(
  'AzureTemplatesManager/UPDATE_AZURE_TEMPLATE_RESET'
)();

// PUT UPDATE AZURE SECRET

export const updateAzureSecretStart = createAction(
  // Type
  'AzureTemplatesManager/UPDATE_AZURE_SECRET_START',
  // Payload
  (data: TUpdateAzureTemplateStart) => data
)();

export const updateAzureSecretSuccess: EmptyActionCreator<string> = createAction(
  'AzureTemplatesManager/UPDATE_AZURE_Secret_SUCCESS'
  // Payload
)();

export const updateAzureSecretFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'AzureTemplatesManager/UPDATE_AZURE_SECRET_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const updateAzureSecretReset: EmptyActionCreator<string> = createAction(
  'AzureTemplatesManager/UPDATE_AZURE_SECRET_RESET'
)();

// DELETE

export const deleteAzureTemplateStart = createAction(
  // Type
  'AzureTemplatesManager/DELETE_AZURE_TEMPLATE_START',
  // Payload
  (data: TDeleteAzureTemplateStart) => data
)();
export const deleteAzureTemplateSuccess: EmptyActionCreator<string> = createAction(
  'AzureTemplatesManager/DELETE_AZURE_TEMPLATE_SUCCESS'
  // Payload
)();
export const deleteAzureTemplateFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'AzureTemplatesManager/DELETE_AZURE_TEMPLATE_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const deleteAzureTemplateReset: EmptyActionCreator<string> = createAction(
  'AzureTemplatesManager/DELETE_AZURE_TEMPLATE_RESET'
)();
  