import {
  ActionType,
  createAction,
  EmptyActionCreator,
  PayloadAction,
} from 'typesafe-actions';

import type { IDefaults } from '@app/redux/typedefs';

import type {
  TPostAccountManagerStart,
  TPostAccountManagerSuccess,
  TPutUpdateUserStart,
  TPutUpdateUserSuccess,
  TPutUpdatePasswordStart,
  TPutUpdatePasswordSuccess,
  TPutUpdateAccessRightsStart,
  TPutUpdateAccessRightsSuccess,
  TGetAllAccountManagersSuccess,
  TGetAccountManagerSuccess,
  TGetAccountManagerStart,
  TDeleteAccountManagerStart,
  TDeleteAccountManagerSuccess,
  TGetAllAccountManagersStart,
  TPutAccountManagerSuccess,
  TPutAccountManagerStart,
} from './accountManager.typeDefs';

export type AccountManagerActions =
  // POST
  | ActionType<typeof postAccountManagerStart>
  | ActionType<typeof postAccountManagerSuccess>
  | ActionType<typeof postAccountManagerFailure>
  | ActionType<typeof postAccountManagerReset>
  // PUT UPDATE USER
  | ActionType<typeof putUpdateUserStart>
  | ActionType<typeof putUpdateUserSuccess>
  | ActionType<typeof putUpdateUserFailure>
  | ActionType<typeof putUpdateUserReset>
  // PUT UPDATE PASSWORD
  | ActionType<typeof putUpdatePasswordStart>
  | ActionType<typeof putUpdatePasswordSuccess>
  | ActionType<typeof putUpdatePasswordFailure>
  | ActionType<typeof putUpdatePasswordReset>
  // PUT ACCESS RIGHTS
  | ActionType<typeof putUpdateAccessRightsStart>
  | ActionType<typeof putUpdateAccessRightsSuccess>
  | ActionType<typeof putUpdateAccessRightsFailure>
  | ActionType<typeof putUpdateAccessRightsReset>
  // GET ALL
  | ActionType<typeof getAllAccountManagersStart>
  | ActionType<typeof getAllAccountManagersSuccess>
  | ActionType<typeof getAllAccountManagersFailure>
  | ActionType<typeof getAllAccountManagersReset>
  // GET
  | ActionType<typeof getAccountManagerStart>
  | ActionType<typeof getAccountManagerSuccess>
  | ActionType<typeof getAccountManagerFailure>
  | ActionType<typeof getAccountManagerReset>
  // DELETE
  | ActionType<typeof deleteAccountManagerStart>
  | ActionType<typeof deleteAccountManagerSuccess>
  | ActionType<typeof deleteAccountManagerFailure>
  | ActionType<typeof deleteAccountManagerReset>
  // PUT
  | ActionType<typeof putAccountManagerStart>
  | ActionType<typeof putAccountManagerSuccess>
  | ActionType<typeof putAccountManagerFailure>
  | ActionType<typeof putAccountManagerReset>;

// POST REGISTER (CREATE USER)

export const postAccountManagerStart = createAction(
  // Type
  'AccountManager/POST_ACCOUNT_MANAGER_START',
  // Payload
  (data: TPostAccountManagerStart) => data
)();

export const postAccountManagerSuccess: EmptyActionCreator<string> = createAction(
  'AccountManager/POST_ACCOUNT_MANAGER_SUCCESS'
  // Payload
)();

export const postAccountManagerFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'AccountManager/POST_ACCOUNT_MANAGER_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const postAccountManagerReset: EmptyActionCreator<string> = createAction(
  'AccountManager/POST_ACCOUNT_MANAGER_RESET'
)();

// PUT UPDATE USER INFORMATION

export const putUpdateUserStart = createAction(
  // Type
  'AccountManager/PUT_UPDATE_USER_START',
  // Payload
  (data: TPutUpdateUserStart) => data
)();

export const putUpdateUserSuccess: EmptyActionCreator<string> = createAction(
  'AccountManager/PUT_UPDATE_USER_SUCCESS'
  // Payload
)();

export const putUpdateUserFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'AccountManager/PUT_UPDATE_USER_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const putUpdateUserReset: EmptyActionCreator<string> = createAction(
  'AccountManager/PUT_UPDATE_USER_RESET'
)();

// PUT UPDATE PASSWORD

export const putUpdatePasswordStart = createAction(
  // Type
  'AccountManager/PUT_UPDATE_PASSWORD_START',
  // Payload
  (data: TPutUpdatePasswordStart) => data
)();

export const putUpdatePasswordSuccess: EmptyActionCreator<string> = createAction(
  'AccountManager/PUT_UPDATE_PASSWORD_SUCCESS'
  // Payload
)();

export const putUpdatePasswordFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'AccountManager/PUT_UPDATE_PASSWORD_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const putUpdatePasswordReset: EmptyActionCreator<string> = createAction(
  'AccountManager/PUT_UPDATE_PASSWORD_RESET'
)();

// PUT UPDATE ACCESS RIGHTS

export const putUpdateAccessRightsStart = createAction(
  // Type
  'AccountManager/PUT_UPDATE_ACCESS_RIGHTS_START',
  // Payload
  (data: TPutUpdateAccessRightsStart) => data
)();

export const putUpdateAccessRightsSuccess: EmptyActionCreator<string> = createAction(
  'AccountManager/PUT_UPDATE_ACCESS_RIGHTS_SUCCESS'
  // Payload
)();

export const putUpdateAccessRightsFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'AccountManager/PUT_UPDATE_ACCESS_RIGHTS_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const putUpdateAccessRightsReset: EmptyActionCreator<string> = createAction(
  'AccountManager/PUT_UPDATE_ACCESS_RIGHTS_RESET'
)();

// GET ALL

export const getAllAccountManagersStart = createAction(
  // Type
  'AccountManager/GET_ALL_ACCOUNT_MANAGERS_START',
  (data: TGetAllAccountManagersStart) => data
)();
export const getAllAccountManagersSuccess: (
  data: TGetAllAccountManagersSuccess
) => PayloadAction<string, TGetAllAccountManagersSuccess> = createAction(
  'AccountManager/GET_ALL_ACCOUNT_MANAGERS_SUCCESS',
  // Payload
  (data: TGetAllAccountManagersSuccess) => data
)();
export const getAllAccountManagersFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'AccountManager/GET_ALL_ACCOUNT_MANAGERS_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getAllAccountManagersReset: EmptyActionCreator<string> = createAction(
  'AccountManager/GET_ALL_ACCOUNT_MANAGERS_RESET'
)();

// GET ONE

export const getAccountManagerStart = createAction(
  // Type
  'AccountManager/GET_ACCOUNT_MANAGER_START',
  // Payload
  (data: TGetAccountManagerStart) => data
)();
export const getAccountManagerSuccess: (
  data: TGetAccountManagerSuccess
) => PayloadAction<string, TGetAccountManagerSuccess> = createAction(
  'AccountManager/GET_ACCOUNT_MANAGER_SUCCESS',
  // Payload
  (data: TGetAccountManagerSuccess) => data
)();
export const getAccountManagerFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'AccountManager/GET_ACCOUNT_MANAGER_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getAccountManagerReset: EmptyActionCreator<string> = createAction(
  'AccountManager/GET_ACCOUNT_MANAGER_RESET'
)();

// DELETE

export const deleteAccountManagerStart = createAction(
  // Type
  'AccountManager/DELETE_ACCOUNT_MANAGER_START',
  // Payload
  (data: TDeleteAccountManagerStart) => data
)();
export const deleteAccountManagerSuccess: (
  data: TDeleteAccountManagerSuccess
) => PayloadAction<string, TDeleteAccountManagerSuccess> = createAction(
  'AccountManager/DELETE_ACCOUNT_MANAGER_SUCCESS',
  // Payload
  (data: TDeleteAccountManagerSuccess) => data
)();
export const deleteAccountManagerFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'AccountManager/DELETE_ACCOUNT_MANAGER_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const deleteAccountManagerReset: EmptyActionCreator<string> = createAction(
  'AccountManager/DELETE_ACCOUNT_MANAGER_RESET'
)();

// PUT (recover account)

export const putAccountManagerStart = createAction(
  // Type
  'AccountManager/PUT_ACCOUNT_MANAGER_START',
  // Payload
  (data: TPutAccountManagerStart) => {
    console.log('putaccountmanager action');
    return data;
  }
)();
export const putAccountManagerSuccess: (
  data: TPutAccountManagerSuccess
) => PayloadAction<string, TPutAccountManagerSuccess> = createAction(
  'AccountManager/PUT_ACCOUNT_MANAGER_SUCCESS',
  // Payload
  (data: TPutAccountManagerSuccess) => data
)();
export const putAccountManagerFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'AccountManager/PUT_ACCOUNT_MANAGER_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const putAccountManagerReset: EmptyActionCreator<string> = createAction(
  'AccountManager/PUT_ACCOUNT_MANAGER_RESET'
)();
