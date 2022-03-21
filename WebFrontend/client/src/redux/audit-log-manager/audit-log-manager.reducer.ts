// tslint:disable: no-null-null-union
import { createReducer } from 'typesafe-actions';

import {
  // GET ALL
  getAllEventsFailure,
  getAllEventsReset,
  getAllEventsStart,
  getAllEventsSuccess,
  // POST
  postLeafEventsFailure,
  postLeafEventsReset,
  postLeafEventsStart,
  postLeafEventsSuccess,
} from './audit-log-manager.actions';

import type {
  IAuditLogManagerData,
  IGetAllEventsSuccess,
} from './audit-log-manager.typeDefs';

import { IDefaults } from '@redux/typedefs';

export interface IEventState {
  // GET ALL
  getAllEventsData: null | IGetAllEventsSuccess;
  getAllEventsError: IDefaults['errorMessage'];
  getAllEventsState: IDefaults['state'];

  // POST
  postLeafEventsData: null | IAuditLogManagerData;
  postLeafEventsError: IDefaults['errorMessage'];
  postLeafEventsState: IDefaults['state'];
}

const INITIAL_STATE: IEventState = {
  // GET ALL
  getAllEventsData: null,
  getAllEventsError: null,
  getAllEventsState: null,

  // POST
  postLeafEventsData: null,
  postLeafEventsError: null,
  postLeafEventsState: null,
};

// tslint:disable-next-line: no-unsafe-any tslint:disable-next-line: typedef
const contactReducer = createReducer(INITIAL_STATE)
  // POST

  .handleAction(
    postLeafEventsStart,
    (state: IEventState): IEventState => ({
      ...state,
      postLeafEventsData: null,
      postLeafEventsError: null,
      postLeafEventsState: 'isLoading',
    })
  )
  .handleAction(
    postLeafEventsSuccess,
    (
      state: IEventState,
      action: { payload: IAuditLogManagerData }
    ): IEventState => ({
      ...state,
      postLeafEventsData: action.payload,
      postLeafEventsError: null,
      postLeafEventsState: 'success',
    })
  )
  .handleAction(
    postLeafEventsFailure,
    (
      state: IEventState,
      action: { payload: IDefaults['errorMessage'] }
    ): IEventState => ({
      ...state,
      postLeafEventsData: null,
      postLeafEventsError: action.payload,
      postLeafEventsState: 'failure',
    })
  )
  .handleAction(
    postLeafEventsReset,
    (state: IEventState): IEventState => ({
      ...state,
      postLeafEventsData: null,
      postLeafEventsError: null,
      postLeafEventsState: null,
    })
  )

  // GET ALL

  .handleAction(
    getAllEventsStart,
    (state: IEventState): IEventState => ({
      ...state,
      getAllEventsData: null,
      getAllEventsError: null,
      getAllEventsState: 'isLoading',
    })
  )
  .handleAction(
    getAllEventsSuccess,
    (
      state: IEventState,
      action: { payload: IGetAllEventsSuccess }
    ): IEventState => ({
      ...state,
      getAllEventsData: action.payload,
      getAllEventsError: null,
      getAllEventsState: 'success',
    })
  )
  .handleAction(
    getAllEventsFailure,
    (
      state: IEventState,
      action: { payload: IDefaults['errorMessage'] }
    ): IEventState => ({
      ...state,
      getAllEventsData: null,
      getAllEventsError: action.payload,
      getAllEventsState: 'failure',
    })
  )
  .handleAction(
    getAllEventsReset,
    (state: IEventState): IEventState => ({
      ...state,
      getAllEventsData: null,
      getAllEventsError: null,
      getAllEventsState: null,
    })
  );

export default contactReducer;
