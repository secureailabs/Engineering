// tslint:disable: no-null-null-union
import { createReducer } from 'typesafe-actions';

import {
  // GET ALL
  getAllDatasetsFailure,
  getAllDatasetsReset,
  getAllDatasetsStart,
  getAllDatasetsSuccess,
  // GET ONE
  getDatasetFailure,
  getDatasetReset,
  getDatasetStart,
  getDatasetSuccess,
  // POST
  postDatasetFailure,
  postDatasetReset,
  postDatasetStart,
  postDatasetSuccess,
} from './dataset.actions';

import type {
  TPostDatasetSuccess,
  TGetAllDatasetsSuccess,
  TGetDatasetSuccess,
  TPatchActivateDatasetSuccess,
  TPatchAcceptDatasetSuccess,
} from './dataset.typeDefs';

import { IDefaults } from '@redux/typedefs';

export interface IDatasetState {
  // GET ALL
  getAllDatasetsData: null | TGetAllDatasetsSuccess;
  getAllDatasetsError: IDefaults['errorMessage'];
  getAllDatasetsState: IDefaults['state'];

  // GET ONE
  getDatasetData: null | TGetDatasetSuccess;
  getDatasetError: IDefaults['errorMessage'];
  getDatasetState: IDefaults['state'];

  // POST
  postDatasetData: null | TPostDatasetSuccess;
  postDatasetError: IDefaults['errorMessage'];
  postDatasetState: IDefaults['state'];
}

const INITIAL_STATE: IDatasetState = {
  // GET ALL
  getAllDatasetsData: null,
  getAllDatasetsError: null,
  getAllDatasetsState: null,

  // GET ONE
  getDatasetData: null,
  getDatasetError: null,
  getDatasetState: null,

  // POST
  postDatasetData: null,
  postDatasetError: null,
  postDatasetState: null,
};

// tslint:disable-next-line: no-unsafe-any tslint:disable-next-line: typedef
const DatasetReducer = createReducer(INITIAL_STATE)
  // POST

  .handleAction(
    postDatasetStart,
    (state: IDatasetState): IDatasetState => ({
      ...state,
      postDatasetData: null,
      postDatasetError: null,
      postDatasetState: 'isLoading',
    })
  )
  .handleAction(
    postDatasetSuccess,
    (
      state: IDatasetState,
      action: { payload: TPostDatasetSuccess }
    ): IDatasetState => ({
      ...state,
      postDatasetData: action.payload,
      postDatasetError: null,
      postDatasetState: 'success',
    })
  )
  .handleAction(
    postDatasetFailure,
    (
      state: IDatasetState,
      action: { payload: IDefaults['errorMessage'] }
    ): IDatasetState => ({
      ...state,
      postDatasetData: null,
      postDatasetError: action.payload,
      postDatasetState: 'failure',
    })
  )
  .handleAction(
    postDatasetReset,
    (state: IDatasetState): IDatasetState => ({
      ...state,
      postDatasetData: null,
      postDatasetError: null,
      postDatasetState: null,
    })
  )

  // GET ALL

  .handleAction(
    getAllDatasetsStart,
    (state: IDatasetState): IDatasetState => ({
      ...state,
      getAllDatasetsData: null,
      getAllDatasetsError: null,
      getAllDatasetsState: 'isLoading',
    })
  )
  .handleAction(
    getAllDatasetsSuccess,
    (
      state: IDatasetState,
      action: { payload: TGetAllDatasetsSuccess }
    ): IDatasetState => ({
      ...state,
      getAllDatasetsData: action.payload,
      getAllDatasetsError: null,
      getAllDatasetsState: 'success',
    })
  )
  .handleAction(
    getAllDatasetsFailure,
    (
      state: IDatasetState,
      action: { payload: IDefaults['errorMessage'] }
    ): IDatasetState => ({
      ...state,
      getAllDatasetsData: null,
      getAllDatasetsError: action.payload,
      getAllDatasetsState: 'failure',
    })
  )
  .handleAction(
    getAllDatasetsReset,
    (state: IDatasetState): IDatasetState => ({
      ...state,
      getAllDatasetsData: null,
      getAllDatasetsError: null,
      getAllDatasetsState: null,
    })
  )

  // GET ONE

  .handleAction(
    getDatasetStart,
    (state: IDatasetState): IDatasetState => ({
      ...state,
      getDatasetData: null,
      getDatasetError: null,
      getDatasetState: 'isLoading',
    })
  )
  .handleAction(
    getDatasetSuccess,
    (
      state: IDatasetState,
      action: { payload: TGetDatasetSuccess }
    ): IDatasetState => ({
      ...state,
      getDatasetData: action.payload,
      getDatasetError: null,
      getDatasetState: 'success',
    })
  )
  .handleAction(
    getDatasetFailure,
    (
      state: IDatasetState,
      action: { payload: IDefaults['errorMessage'] }
    ): IDatasetState => ({
      ...state,
      getDatasetData: null,
      getDatasetError: action.payload,
      getDatasetState: 'failure',
    })
  )
  .handleAction(
    getDatasetReset,
    (state: IDatasetState): IDatasetState => ({
      ...state,
      getDatasetData: null,
      getDatasetError: null,
      getDatasetState: null,
    })
  );

export default DatasetReducer;
