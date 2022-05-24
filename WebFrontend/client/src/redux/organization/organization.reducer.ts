// tslint:disable: no-null-null-union
import { createReducer } from 'typesafe-actions';

import {
  // GET ONE
  getOrganizationFailure,
  getOrganizationReset,
  getOrganizationStart,
  getOrganizationSuccess,
  // PUT
  putOrganizationFailure,
  putOrganizationReset,
  putOrganizationStart,
  putOrganizationSuccess,
} from './organization.actions';

import type {
  TGetOrganizationSuccess,
  TPutOrganizationSuccess,
} from './organization.typeDefs';

import { IDefaults } from '@app/redux/typedefs';

export interface IOrganizationState {
  // GET ONE
  getOrganizationData: null | TGetOrganizationSuccess;
  getOrganizationError: IDefaults['errorMessage'];
  getOrganizationState: IDefaults['state'];

  // PUT
  putOrganizationData: null | TPutOrganizationSuccess;
  putOrganizationError: IDefaults['errorMessage'];
  putOrganizationState: IDefaults['state'];
}

const INITIAL_STATE: IOrganizationState = {
  // GET ONE
  getOrganizationData: null,
  getOrganizationError: null,
  getOrganizationState: null,

  // PUT
  putOrganizationData: null,
  putOrganizationError: null,
  putOrganizationState: null,
};

// tslint:disable-next-line: no-unsafe-any tslint:disable-next-line: typedef
const OrganizationReducer = createReducer(INITIAL_STATE)
  // GET ONE

  .handleAction(
    getOrganizationStart,
    (state: IOrganizationState): IOrganizationState => ({
      ...state,
      getOrganizationData: null,
      getOrganizationError: null,
      getOrganizationState: 'isLoading',
    })
  )
  .handleAction(
    getOrganizationSuccess,
    (
      state: IOrganizationState,
      action: { payload: TGetOrganizationSuccess }
    ): IOrganizationState => ({
      ...state,
      getOrganizationData: action.payload,
      getOrganizationError: null,
      getOrganizationState: 'success',
    })
  )
  .handleAction(
    getOrganizationFailure,
    (
      state: IOrganizationState,
      action: { payload: IDefaults['errorMessage'] }
    ): IOrganizationState => ({
      ...state,
      getOrganizationData: null,
      getOrganizationError: action.payload,
      getOrganizationState: 'failure',
    })
  )
  .handleAction(
    getOrganizationReset,
    (state: IOrganizationState): IOrganizationState => ({
      ...state,
      getOrganizationData: null,
      getOrganizationError: null,
      getOrganizationState: null,
    })
  )

  // PUT

  .handleAction(
    putOrganizationStart,
    (state: IOrganizationState): IOrganizationState => ({
      ...state,
      putOrganizationData: null,
      putOrganizationError: null,
      putOrganizationState: 'isLoading',
    })
  )
  .handleAction(
    putOrganizationSuccess,
    (
      state: IOrganizationState,
      action: { payload: TPutOrganizationSuccess }
    ): IOrganizationState => ({
      ...state,
      putOrganizationData: action.payload,
      putOrganizationError: null,
      putOrganizationState: 'success',
    })
  )
  .handleAction(
    putOrganizationFailure,
    (
      state: IOrganizationState,
      action: { payload: IDefaults['errorMessage'] }
    ): IOrganizationState => ({
      ...state,
      putOrganizationData: null,
      putOrganizationError: action.payload,
      putOrganizationState: 'failure',
    })
  )
  .handleAction(
    putOrganizationReset,
    (state: IOrganizationState): IOrganizationState => ({
      ...state,
      putOrganizationData: null,
      putOrganizationError: null,
      putOrganizationState: null,
    })
  );

export default OrganizationReducer;
