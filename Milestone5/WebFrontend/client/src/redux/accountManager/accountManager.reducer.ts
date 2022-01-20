// tslint:disable: no-null-null-union
import { createReducer } from 'typesafe-actions';

import {
  // GET ALL
  getAllAccountManagersFailure,
  getAllAccountManagersReset,
  getAllAccountManagersStart,
  getAllAccountManagersSuccess,
  // GET ONE
  getAccountManagerFailure,
  getAccountManagerReset,
  getAccountManagerStart,
  getAccountManagerSuccess,
  // PUT UPDATE USER
  putUpdateUserFailure,
  putUpdateUserReset,
  putUpdateUserStart,
  putUpdateUserSuccess,

  // PUT UPDATE PASSWORD
  putUpdatePasswordFailure,
  putUpdatePasswordReset,
  putUpdatePasswordStart,
  putUpdatePasswordSuccess,

  // PUT UPDATE ACCESS RIGHTS
  putUpdateAccessRightsFailure,
  putUpdateAccessRightsReset,
  putUpdateAccessRightsStart,
  putUpdateAccessRightsSuccess,

  // POST
  postAccountManagerFailure,
  postAccountManagerReset,
  postAccountManagerStart,
  postAccountManagerSuccess,

  // DELETE
  deleteAccountManagerFailure,
  deleteAccountManagerReset,
  deleteAccountManagerStart,
  deleteAccountManagerSuccess,

  // PUT (reopen account)
  putAccountManagerFailure,
  putAccountManagerReset,
  putAccountManagerStart,
  putAccountManagerSuccess
} from './accountManager.actions';

import type {
  TPostAccountManagerSuccess,
  TGetAllAccountManagersSuccess,
  TGetAccountManagerSuccess,
  TPutUpdateUserSuccess,
  TPutUpdatePasswordSuccess,
  TPutUpdateAccessRightsSuccess,
  TDeleteAccountManagerSuccess,
  TPutAccountManagerSuccess,
} from './accountManager.typeDefs';

import { IDefaults } from '@redux/typedefs';

export interface IAccountManagerState {
  // GET ALL
  getAllAccountManagersData: null | TGetAllAccountManagersSuccess;
  getAllAccountManagersError: IDefaults['errorMessage'];
  getAllAccountManagersState: IDefaults['state'];

  // GET ONE
  getAccountManagerData: null | TGetAccountManagerSuccess;
  getAccountManagerError: IDefaults['errorMessage'];
  getAccountManagerState: IDefaults['state'];

  // PUT UPDATE USER
  putUpdateUserData: null | TPutUpdateUserSuccess;
  putUpdateUserError: IDefaults['errorMessage'];
  putUpdateUserState: IDefaults['state'];

  // PUT UPDATE PASSWORD
  putUpdatePasswordData: null | TPutUpdatePasswordSuccess;
  putUpdatePasswordError: IDefaults['errorMessage'];
  putUpdatePasswordState: IDefaults['state'];

  // PUT UPDATE ACCESS RIGHTS
  putUpdateAccessRightsData: null | TPutUpdateAccessRightsSuccess;
  putUpdateAccessRightsError: IDefaults['errorMessage'];
  putUpdateAccessRightsState: IDefaults['state'];

  // POST
  postAccountManagerData: null | TPostAccountManagerSuccess;
  postAccountManagerError: IDefaults['errorMessage'];
  postAccountManagerState: IDefaults['state'];

  // DELETE
  deleteAccountManagerData: null | TDeleteAccountManagerSuccess;
  deleteAccountManagerError: IDefaults['errorMessage'];
  deleteAccountManagerState: IDefaults['state'];

  // PUT (reopen account)
  putAccountManagerData: null | TPutAccountManagerSuccess;
  putAccountManagerError: IDefaults['errorMessage'];
  putAccountManagerState: IDefaults['state'];
}

const INITIAL_STATE: IAccountManagerState = {
  // GET ALL
  getAllAccountManagersData: null,
  getAllAccountManagersError: null,
  getAllAccountManagersState: null,

  // GET ONE
  getAccountManagerData: null,
  getAccountManagerError: null,
  getAccountManagerState: null,

  // PUT UPDATE USER
  putUpdateUserData: null,
  putUpdateUserError: null,
  putUpdateUserState: null,

  // PUT UPDATE PASSWORD
  putUpdatePasswordData: null,
  putUpdatePasswordError: null,
  putUpdatePasswordState: null,

  // PUT UPDATE ACCESS RIGHTS
  putUpdateAccessRightsData: null,
  putUpdateAccessRightsError: null,
  putUpdateAccessRightsState: null,

  // POST
  postAccountManagerData: null,
  postAccountManagerError: null,
  postAccountManagerState: null,

  // DELETE
  deleteAccountManagerData: null,
  deleteAccountManagerError: null,
  deleteAccountManagerState: null,

  // PUT (reopen account)
  putAccountManagerData: null,
  putAccountManagerError: null,
  putAccountManagerState: null,
};

// tslint:disable-next-line: no-unsafe-any tslint:disable-next-line: typedef
const AccountManagerReducer = createReducer(INITIAL_STATE)
  // POST

  .handleAction(
    postAccountManagerStart,
    (state: IAccountManagerState): IAccountManagerState => ({
      ...state,
      postAccountManagerData: null,
      postAccountManagerError: null,
      postAccountManagerState: 'isLoading',
    })
  )
  .handleAction(
    postAccountManagerSuccess,
    (
      state: IAccountManagerState,
      action: { payload: TPostAccountManagerSuccess }
    ): IAccountManagerState => ({
      ...state,
      postAccountManagerData: action.payload,
      postAccountManagerError: null,
      postAccountManagerState: 'success',
    })
  )
  .handleAction(
    postAccountManagerFailure,
    (
      state: IAccountManagerState,
      action: { payload: IDefaults['errorMessage'] }
    ): IAccountManagerState => ({
      ...state,
      postAccountManagerData: null,
      postAccountManagerError: action.payload,
      postAccountManagerState: 'failure',
    })
  )
  .handleAction(
    postAccountManagerReset,
    (state: IAccountManagerState): IAccountManagerState => ({
      ...state,
      postAccountManagerData: null,
      postAccountManagerError: null,
      postAccountManagerState: null,
    })
  )

  // GET ALL

  .handleAction(
    getAllAccountManagersStart,
    (state: IAccountManagerState): IAccountManagerState => ({
      ...state,
      getAllAccountManagersData: null,
      getAllAccountManagersError: null,
      getAllAccountManagersState: 'isLoading',
    })
  )
  .handleAction(
    getAllAccountManagersSuccess,
    (
      state: IAccountManagerState,
      action: { payload: TGetAllAccountManagersSuccess }
    ): IAccountManagerState => ({
      ...state,
      getAllAccountManagersData: action.payload,
      getAllAccountManagersError: null,
      getAllAccountManagersState: 'success',
    })
  )
  .handleAction(
    getAllAccountManagersFailure,
    (
      state: IAccountManagerState,
      action: { payload: IDefaults['errorMessage'] }
    ): IAccountManagerState => ({
      ...state,
      getAllAccountManagersData: null,
      getAllAccountManagersError: action.payload,
      getAllAccountManagersState: 'failure',
    })
  )
  .handleAction(
    getAllAccountManagersReset,
    (state: IAccountManagerState): IAccountManagerState => ({
      ...state,
      getAllAccountManagersData: null,
      getAllAccountManagersError: null,
      getAllAccountManagersState: null,
    })
  )

  // GET ONE

  .handleAction(
    getAccountManagerStart,
    (state: IAccountManagerState): IAccountManagerState => ({
      ...state,
      getAccountManagerData: null,
      getAccountManagerError: null,
      getAccountManagerState: 'isLoading',
    })
  )
  .handleAction(
    getAccountManagerSuccess,
    (
      state: IAccountManagerState,
      action: { payload: TGetAccountManagerSuccess }
    ): IAccountManagerState => ({
      ...state,
      getAccountManagerData: action.payload,
      getAccountManagerError: null,
      getAccountManagerState: 'success',
    })
  )
  .handleAction(
    getAccountManagerFailure,
    (
      state: IAccountManagerState,
      action: { payload: IDefaults['errorMessage'] }
    ): IAccountManagerState => ({
      ...state,
      getAccountManagerData: null,
      getAccountManagerError: action.payload,
      getAccountManagerState: 'failure',
    })
  )
  .handleAction(
    getAccountManagerReset,
    (state: IAccountManagerState): IAccountManagerState => ({
      ...state,
      getAccountManagerData: null,
      getAccountManagerError: null,
      getAccountManagerState: null,
    })
  )

  // PUT UPDATE USER

  .handleAction(
    putUpdateUserStart,
    (state: IAccountManagerState): IAccountManagerState => ({
      ...state,
      putUpdateUserData: null,
      putUpdateUserError: null,
      putUpdateUserState: 'isLoading',
    })
  )
  .handleAction(
    putUpdateUserSuccess,
    (
      state: IAccountManagerState,
      action: { payload: TPutUpdateUserSuccess }
    ): IAccountManagerState => ({
      ...state,
      putUpdateUserData: action.payload,
      putUpdateUserError: null,
      putUpdateUserState: 'success',
    })
  )
  .handleAction(
    putUpdateUserFailure,
    (
      state: IAccountManagerState,
      action: { payload: IDefaults['errorMessage'] }
    ): IAccountManagerState => ({
      ...state,
      putUpdateUserData: null,
      putUpdateUserError: action.payload,
      putUpdateUserState: 'failure',
    })
  )
  .handleAction(
    putUpdateUserReset,
    (state: IAccountManagerState): IAccountManagerState => ({
      ...state,
      putUpdateUserData: null,
      putUpdateUserError: null,
      putUpdateUserState: null,
    })
  )

  // PUT UPDATE PASSWORD

  .handleAction(
    putUpdatePasswordStart,
    (state: IAccountManagerState): IAccountManagerState => ({
      ...state,
      putUpdatePasswordData: null,
      putUpdatePasswordError: null,
      putUpdatePasswordState: 'isLoading',
    })
  )
  .handleAction(
    putUpdatePasswordSuccess,
    (
      state: IAccountManagerState,
      action: { payload: TPutUpdatePasswordSuccess }
    ): IAccountManagerState => ({
      ...state,
      putUpdatePasswordData: action.payload,
      putUpdatePasswordError: null,
      putUpdatePasswordState: 'success',
    })
  )
  .handleAction(
    putUpdatePasswordFailure,
    (
      state: IAccountManagerState,
      action: { payload: IDefaults['errorMessage'] }
    ): IAccountManagerState => ({
      ...state,
      putUpdatePasswordData: null,
      putUpdatePasswordError: action.payload,
      putUpdatePasswordState: 'failure',
    })
  )
  .handleAction(
    putUpdatePasswordReset,
    (state: IAccountManagerState): IAccountManagerState => ({
      ...state,
      putUpdatePasswordData: null,
      putUpdatePasswordError: null,
      putUpdatePasswordState: null,
    })
  )

  // PUT UPDATE ACCESS RIGHTS

  .handleAction(
    putUpdateAccessRightsStart,
    (state: IAccountManagerState): IAccountManagerState => ({
      ...state,
      putUpdateAccessRightsData: null,
      putUpdateAccessRightsError: null,
      putUpdateAccessRightsState: 'isLoading',
    })
  )
  .handleAction(
    putUpdateAccessRightsSuccess,
    (
      state: IAccountManagerState,
      action: { payload: TPutUpdateAccessRightsSuccess }
    ): IAccountManagerState => ({
      ...state,
      putUpdateAccessRightsData: action.payload,
      putUpdateAccessRightsError: null,
      putUpdateAccessRightsState: 'success',
    })
  )
  .handleAction(
    putUpdateAccessRightsFailure,
    (
      state: IAccountManagerState,
      action: { payload: IDefaults['errorMessage'] }
    ): IAccountManagerState => ({
      ...state,
      putUpdateAccessRightsData: null,
      putUpdateAccessRightsError: action.payload,
      putUpdateAccessRightsState: 'failure',
    })
  )
  .handleAction(
    putUpdateAccessRightsReset,
    (state: IAccountManagerState): IAccountManagerState => ({
      ...state,
      putUpdateAccessRightsData: null,
      putUpdateAccessRightsError: null,
      putUpdateAccessRightsState: null,
    })
  )

  // DELETE

  .handleAction(
    deleteAccountManagerStart,
    (state: IAccountManagerState): IAccountManagerState => ({
      ...state,
      deleteAccountManagerData: null,
      deleteAccountManagerError: null,
      deleteAccountManagerState: 'isLoading',
    })
  )
  .handleAction(
    deleteAccountManagerSuccess,
    (
      state: IAccountManagerState,
      action: { payload: TDeleteAccountManagerSuccess }
    ): IAccountManagerState => ({
      ...state,
      deleteAccountManagerData: action.payload,
      deleteAccountManagerError: null,
      deleteAccountManagerState: 'success',
    })
  )
  .handleAction(
    deleteAccountManagerFailure,
    (
      state: IAccountManagerState,
      action: { payload: IDefaults['errorMessage'] }
    ): IAccountManagerState => ({
      ...state,
      deleteAccountManagerData: null,
      deleteAccountManagerError: action.payload,
      deleteAccountManagerState: 'failure',
    })
  )
  .handleAction(
    deleteAccountManagerReset,
    (state: IAccountManagerState): IAccountManagerState => ({
      ...state,
      deleteAccountManagerData: null,
      deleteAccountManagerError: null,
      deleteAccountManagerState: null,
    })
  )

  // PUT (reopen account)

  .handleAction(
    putAccountManagerStart,
    (state: IAccountManagerState): IAccountManagerState => ({
      ...state,
      putAccountManagerData: null,
      putAccountManagerError: null,
      putAccountManagerState: 'isLoading',
    })
  )
  .handleAction(
    putAccountManagerSuccess,
    (
      state: IAccountManagerState,
      action: { payload: TPutAccountManagerSuccess }
    ): IAccountManagerState => ({
      ...state,
      putAccountManagerData: action.payload,
      putAccountManagerError: null,
      putAccountManagerState: 'success',
    })
  )
  .handleAction(
    putAccountManagerFailure,
    (
      state: IAccountManagerState,
      action: { payload: IDefaults['errorMessage'] }
    ): IAccountManagerState => ({
      ...state,
      putAccountManagerData: null,
      putAccountManagerError: action.payload,
      putAccountManagerState: 'failure',
    })
  )
  .handleAction(
    putAccountManagerReset,
    (state: IAccountManagerState): IAccountManagerState => ({
      ...state,
      putAccountManagerData: null,
      putAccountManagerError: null,
      putAccountManagerState: null,
    })
  );

export default AccountManagerReducer;
