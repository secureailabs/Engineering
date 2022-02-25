// tslint:disable: no-null-null-union
import { createReducer } from 'typesafe-actions';

import {
  // GET ALL
  getAllUnifiedRegistriesFailure,
  getAllUnifiedRegistriesReset,
  getAllUnifiedRegistriesStart,
  getAllUnifiedRegistriesSuccess,
  // GET ONE
  getUnifiedRegistryFailure,
  getUnifiedRegistryReset,
  getUnifiedRegistryStart,
  getUnifiedRegistrySuccess,
  // POST
  postUnifiedRegistryFailure,
  postUnifiedRegistryReset,
  postUnifiedRegistryStart,
  postUnifiedRegistrySuccess,

  // DELETE
  deleteUnifiedRegistryFailure,
  deleteUnifiedRegistryReset,
  deleteUnifiedRegistryStart,
  deleteUnifiedRegistrySuccess,

  // PUT (reopen account)
  putUnifiedRegistryFailure,
  putUnifiedRegistryReset,
  putUnifiedRegistryStart,
  putUnifiedRegistrySuccess,
} from './unifiedRegistry.actions';

import type {
  TPostUnifiedRegistrySuccess,
  TGetAllUnifiedRegistriesSuccess,
  TGetUnifiedRegistrySuccess,
  TDeleteUnifiedRegistrySuccess,
  TPutUnifiedRegistrySuccess,
} from './unifiedRegistry.types';

import { IDefaults } from '@redux/typedefs';

export interface IUnifiedRegistryState {
  // GET ALL
  getAllUnifiedRegistriesData: null | TGetAllUnifiedRegistriesSuccess;
  getAllUnifiedRegistriesError: IDefaults['errorMessage'];
  getAllUnifiedRegistriesState: IDefaults['state'];

  // GET ONE
  getUnifiedRegistryData: null | TGetUnifiedRegistrySuccess;
  getUnifiedRegistryError: IDefaults['errorMessage'];
  getUnifiedRegistryState: IDefaults['state'];
  // POST
  postUnifiedRegistryData: null | TPostUnifiedRegistrySuccess;
  postUnifiedRegistryError: IDefaults['errorMessage'];
  postUnifiedRegistryState: IDefaults['state'];

  // DELETE
  deleteUnifiedRegistryData: null | TDeleteUnifiedRegistrySuccess;
  deleteUnifiedRegistryError: IDefaults['errorMessage'];
  deleteUnifiedRegistryState: IDefaults['state'];

  // PUT (reopen account)
  putUnifiedRegistryData: null | TPutUnifiedRegistrySuccess;
  putUnifiedRegistryError: IDefaults['errorMessage'];
  putUnifiedRegistryState: IDefaults['state'];
}

const INITIAL_STATE: IUnifiedRegistryState = {
  // GET ALL
  getAllUnifiedRegistriesData: null,
  getAllUnifiedRegistriesError: null,
  getAllUnifiedRegistriesState: null,

  // GET ONE
  getUnifiedRegistryData: null,
  getUnifiedRegistryError: null,
  getUnifiedRegistryState: null,
  // POST
  postUnifiedRegistryData: null,
  postUnifiedRegistryError: null,
  postUnifiedRegistryState: null,

  // DELETE
  deleteUnifiedRegistryData: null,
  deleteUnifiedRegistryError: null,
  deleteUnifiedRegistryState: null,

  // PUT (reopen account)
  putUnifiedRegistryData: null,
  putUnifiedRegistryError: null,
  putUnifiedRegistryState: null,
};

// tslint:disable-next-line: no-unsafe-any tslint:disable-next-line: typedef
const UnifiedRegistryReducer = createReducer(INITIAL_STATE)
  // POST

  .handleAction(
    postUnifiedRegistryStart,
    (state: IUnifiedRegistryState): IUnifiedRegistryState => ({
      ...state,
      postUnifiedRegistryData: null,
      postUnifiedRegistryError: null,
      postUnifiedRegistryState: 'isLoading',
    })
  )
  .handleAction(
    postUnifiedRegistrySuccess,
    (
      state: IUnifiedRegistryState,
      action: { payload: TPostUnifiedRegistrySuccess }
    ): IUnifiedRegistryState => ({
      ...state,
      postUnifiedRegistryData: action.payload,
      postUnifiedRegistryError: null,
      postUnifiedRegistryState: 'success',
    })
  )
  .handleAction(
    postUnifiedRegistryFailure,
    (
      state: IUnifiedRegistryState,
      action: { payload: IDefaults['errorMessage'] }
    ): IUnifiedRegistryState => ({
      ...state,
      postUnifiedRegistryData: null,
      postUnifiedRegistryError: action.payload,
      postUnifiedRegistryState: 'failure',
    })
  )
  .handleAction(
    postUnifiedRegistryReset,
    (state: IUnifiedRegistryState): IUnifiedRegistryState => ({
      ...state,
      postUnifiedRegistryData: null,
      postUnifiedRegistryError: null,
      postUnifiedRegistryState: null,
    })
  )

  // GET ALL

  .handleAction(
    getAllUnifiedRegistriesStart,
    (state: IUnifiedRegistryState): IUnifiedRegistryState => ({
      ...state,
      getAllUnifiedRegistriesData: null,
      getAllUnifiedRegistriesError: null,
      getAllUnifiedRegistriesState: 'isLoading',
    })
  )
  .handleAction(
    getAllUnifiedRegistriesSuccess,
    (
      state: IUnifiedRegistryState,
      action: { payload: TGetAllUnifiedRegistriesSuccess }
    ): IUnifiedRegistryState => ({
      ...state,
      getAllUnifiedRegistriesData: action.payload,
      getAllUnifiedRegistriesError: null,
      getAllUnifiedRegistriesState: 'success',
    })
  )
  .handleAction(
    getAllUnifiedRegistriesFailure,
    (
      state: IUnifiedRegistryState,
      action: { payload: IDefaults['errorMessage'] }
    ): IUnifiedRegistryState => ({
      ...state,
      getAllUnifiedRegistriesData: null,
      getAllUnifiedRegistriesError: action.payload,
      getAllUnifiedRegistriesState: 'failure',
    })
  )
  .handleAction(
    getAllUnifiedRegistriesReset,
    (state: IUnifiedRegistryState): IUnifiedRegistryState => ({
      ...state,
      getAllUnifiedRegistriesData: null,
      getAllUnifiedRegistriesError: null,
      getAllUnifiedRegistriesState: null,
    })
  )

  // GET ONE

  .handleAction(
    getUnifiedRegistryStart,
    (state: IUnifiedRegistryState): IUnifiedRegistryState => ({
      ...state,
      getUnifiedRegistryData: null,
      getUnifiedRegistryError: null,
      getUnifiedRegistryState: 'isLoading',
    })
  )
  .handleAction(
    getUnifiedRegistrySuccess,
    (
      state: IUnifiedRegistryState,
      action: { payload: TGetUnifiedRegistrySuccess }
    ): IUnifiedRegistryState => ({
      ...state,
      getUnifiedRegistryData: action.payload,
      getUnifiedRegistryError: null,
      getUnifiedRegistryState: 'success',
    })
  )
  .handleAction(
    getUnifiedRegistryFailure,
    (
      state: IUnifiedRegistryState,
      action: { payload: IDefaults['errorMessage'] }
    ): IUnifiedRegistryState => ({
      ...state,
      getUnifiedRegistryData: null,
      getUnifiedRegistryError: action.payload,
      getUnifiedRegistryState: 'failure',
    })
  )
  .handleAction(
    getUnifiedRegistryReset,
    (state: IUnifiedRegistryState): IUnifiedRegistryState => ({
      ...state,
      getUnifiedRegistryData: null,
      getUnifiedRegistryError: null,
      getUnifiedRegistryState: null,
    })
  )
  // DELETE

  .handleAction(
    deleteUnifiedRegistryStart,
    (state: IUnifiedRegistryState): IUnifiedRegistryState => ({
      ...state,
      deleteUnifiedRegistryData: null,
      deleteUnifiedRegistryError: null,
      deleteUnifiedRegistryState: 'isLoading',
    })
  )
  .handleAction(
    deleteUnifiedRegistrySuccess,
    (
      state: IUnifiedRegistryState,
      action: { payload: TDeleteUnifiedRegistrySuccess }
    ): IUnifiedRegistryState => ({
      ...state,
      deleteUnifiedRegistryData: action.payload,
      deleteUnifiedRegistryError: null,
      deleteUnifiedRegistryState: 'success',
    })
  )
  .handleAction(
    deleteUnifiedRegistryFailure,
    (
      state: IUnifiedRegistryState,
      action: { payload: IDefaults['errorMessage'] }
    ): IUnifiedRegistryState => ({
      ...state,
      deleteUnifiedRegistryData: null,
      deleteUnifiedRegistryError: action.payload,
      deleteUnifiedRegistryState: 'failure',
    })
  )
  .handleAction(
    deleteUnifiedRegistryReset,
    (state: IUnifiedRegistryState): IUnifiedRegistryState => ({
      ...state,
      deleteUnifiedRegistryData: null,
      deleteUnifiedRegistryError: null,
      deleteUnifiedRegistryState: null,
    })
  )

  // PUT (reopen account)

  .handleAction(
    putUnifiedRegistryStart,
    (state: IUnifiedRegistryState): IUnifiedRegistryState => ({
      ...state,
      putUnifiedRegistryData: null,
      putUnifiedRegistryError: null,
      putUnifiedRegistryState: 'isLoading',
    })
  )
  .handleAction(
    putUnifiedRegistrySuccess,
    (
      state: IUnifiedRegistryState,
      action: { payload: TPutUnifiedRegistrySuccess }
    ): IUnifiedRegistryState => ({
      ...state,
      putUnifiedRegistryData: action.payload,
      putUnifiedRegistryError: null,
      putUnifiedRegistryState: 'success',
    })
  )
  .handleAction(
    putUnifiedRegistryFailure,
    (
      state: IUnifiedRegistryState,
      action: { payload: IDefaults['errorMessage'] }
    ): IUnifiedRegistryState => ({
      ...state,
      putUnifiedRegistryData: null,
      putUnifiedRegistryError: action.payload,
      putUnifiedRegistryState: 'failure',
    })
  )
  .handleAction(
    putUnifiedRegistryReset,
    (state: IUnifiedRegistryState): IUnifiedRegistryState => ({
      ...state,
      putUnifiedRegistryData: null,
      putUnifiedRegistryError: null,
      putUnifiedRegistryState: null,
    })
  );

export default UnifiedRegistryReducer;
