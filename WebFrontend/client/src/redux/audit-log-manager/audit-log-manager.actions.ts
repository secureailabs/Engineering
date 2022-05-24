import {
  ActionType,
  createAction,
  EmptyActionCreator,
  PayloadAction,
} from 'typesafe-actions';

import type { IDefaults } from '@app/redux/typedefs';

import {
  IGetAllEventsStart,
  IPostLeafEventsStart,
} from './audit-log-manager.typeDefs';

export type auditLogManager =
  | ActionType<typeof postLeafEventsStart>
  | ActionType<typeof postLeafEventsSuccess>
  | ActionType<typeof postLeafEventsFailure>
  | ActionType<typeof postLeafEventsReset>
  | ActionType<typeof getAllEventsStart>
  | ActionType<typeof getAllEventsSuccess>
  | ActionType<typeof getAllEventsFailure>
  | ActionType<typeof getAllEventsReset>;

// POST

export const postLeafEventsStart = createAction(
  // Type
  'auditLogManager/POST_LEAF_EVENTS_START',
  // Payload
  (data: IPostLeafEventsStart) => data
)();

export const postLeafEventsSuccess: EmptyActionCreator<string> = createAction(
  'auditLogManager/POST_LEAF_EVENTS_SUCCESS'
  // Payload
)();

export const postLeafEventsFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'auditLogManager/POST_LEAF_EVENTS_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const postLeafEventsReset: EmptyActionCreator<string> = createAction(
  'auditLogManager/POST_LEAF_EVENTS_RESET'
)();

// GET ALL

export const getAllEventsStart = createAction(
  // Type
  'auditLogManager/GET_ALL_EVENTS_START',
  // Payload
  (data: IGetAllEventsStart) => data
)();

export const getAllEventsSuccess: EmptyActionCreator<string> = createAction(
  'auditLogManager/GET_ALL_EVENTS_SUCCESS'
  // Payload
)();

export const getAllEventsFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'auditLogManager/GET_ALL_EVENTS_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getAllEventsReset: EmptyActionCreator<string> = createAction(
  'auditLogManager/GET_ALL_EVENTS_RESET'
)();
