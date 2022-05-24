//@ts-nocheck
import {
  ActionType,
  createAction,
  EmptyActionCreator,
  PayloadAction,
} from 'typesafe-actions';

import type { IDefaults } from '@app/redux/typedefs';

import type {
  TPutOrganizationStart,
  TGetOrganizationSuccess,
} from './organization.typeDefs';

export type OrganizationActions =
  // PUT
  | ActionType<typeof putOrganizationStart>
  | ActionType<typeof putOrganizationSuccess>
  | ActionType<typeof putOrganizationFailure>
  | ActionType<typeof putOrganizationReset>
  // GET
  | ActionType<typeof getOrganizationStart>
  | ActionType<typeof getOrganizationSuccess>
  | ActionType<typeof getOrganizationFailure>
  | ActionType<typeof getOrganizationReset>;

// PUT

export const putOrganizationStart = createAction(
  // Type
  'Organization/PUT_ORGANIZATION_START',
  // Payload
  (data: TPutOrganizationStart) => data
)();

export const putOrganizationSuccess: EmptyActionCreator<string> = createAction(
  'Organization/PUT_ORGANIZATION_SUCCESS'
  // Payload
)();

export const putOrganizationFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'Organization/PUT_ORGANIZATION_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const putOrganizationReset: EmptyActionCreator<string> = createAction(
  'Organization/PUT_ORGANIZATION_RESET'
)();

// GET ONE

export const getOrganizationStart = createAction(
  // Type
  'Organization/GET_ORGANIZATION_START'
)();
export const getOrganizationSuccess: (
  data: TGetOrganizationSuccess
) => PayloadAction<string, TGetOrganizationSuccess> = createAction(
  'Organization/GET_ORGANIZATION_SUCCESS',
  // Payload
  (data: TGetOrganizationSuccess) => data
)();
export const getOrganizationFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'Organization/GET_ORGANIZATION_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getOrganizationReset: EmptyActionCreator<string> = createAction(
  'Organization/GET_ORGANIZATION_RESET'
)();
