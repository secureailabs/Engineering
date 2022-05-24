//@ts-nocheck
import {
  ActionType,
  createAction,
  EmptyActionCreator,
  PayloadAction,
} from 'typesafe-actions';

import type { IDefaults } from '@app/redux/typedefs';

import type {
  TPostFeedStart,
  TPostFeedSuccess,
  TPutFeedStart,
  TGetAllFeedsSuccess,
  TGetFeedSuccess,
  TGetFeedStart,
  TDeleteFeedStart,
  TDeleteFeedSuccess,
} from './feed.types';

export type feedActions =
  // POST
  | ActionType<typeof postFeedStart>
  | ActionType<typeof postFeedSuccess>
  | ActionType<typeof postFeedFailure>
  | ActionType<typeof postFeedReset>
  // PUT ACTIVATE
  | ActionType<typeof putFeedStart>
  | ActionType<typeof putFeedSuccess>
  | ActionType<typeof putFeedFailure>
  | ActionType<typeof putFeedReset>
  // GET ALL
  | ActionType<typeof getAllFeedsStart>
  | ActionType<typeof getAllFeedsSuccess>
  | ActionType<typeof getAllFeedsFailure>
  | ActionType<typeof getAllFeedsReset>
  // GET
  | ActionType<typeof getFeedStart>
  | ActionType<typeof getFeedSuccess>
  | ActionType<typeof getFeedFailure>
  | ActionType<typeof getFeedReset>
  // GET
  | ActionType<typeof deleteFeedStart>
  | ActionType<typeof deleteFeedSuccess>
  | ActionType<typeof deleteFeedFailure>
  | ActionType<typeof deleteFeedReset>;

// POST REGISTER

export const postFeedStart = createAction(
  'feed/POST_FEED_START',
  (data: TPostFeedStart) => data
)();
export const postFeedSuccess: EmptyActionCreator<string> = createAction(
  'feed/POST_FEED_SUCCESS'
)();
export const postFeedFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'feed/POST_FEED_FAILURE',
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const postFeedReset: EmptyActionCreator<string> = createAction(
  'feed/POST_FEED_RESET'
)();

// PUT
export const putFeedStart = createAction(
  'feed/PUT_FEED_START',
  (data: TPutFeedStart) => data
)();
export const putFeedSuccess: EmptyActionCreator<string> = createAction(
  'feed/PUT_FEED_SUCCESS'
)();
export const putFeedFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'feed/PUT_FEED_FAILURE',
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const putFeedReset: EmptyActionCreator<string> = createAction(
  'feed/PUT_FEED_RESET'
)();

// GET ALL
export const getAllFeedsStart = createAction('feed/GET_ALL_FEEDS_START')();
export const getAllFeedsSuccess: (
  data: TGetAllFeedsSuccess
) => PayloadAction<string, TGetAllFeedsSuccess> = createAction(
  'feed/GET_ALL_FEEDS_SUCCESS',
  (data: TGetAllFeedsSuccess) => data
)();
export const getAllFeedsFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'feed/GET_ALL_FEEDS_FAILURE',
  // Payload
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getAllFeedsReset: EmptyActionCreator<string> = createAction(
  'feed/GET_ALL_FEEDS_RESET'
)();

// GET ONE
export const getFeedStart = createAction(
  'feed/GET_FEED_START',
  (data: TGetFeedStart) => data
)();
export const getFeedSuccess: (
  data: TGetFeedSuccess
) => PayloadAction<string, TGetFeedSuccess> = createAction(
  'feed/GET_FEED_SUCCESS',
  (data: TGetFeedSuccess) => data
)();
export const getFeedFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'feed/GET_FEED_FAILURE',
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const getFeedReset: EmptyActionCreator<string> = createAction(
  'feed/GET_FEED_RESET'
)();

// DELETE
export const deleteFeedStart = createAction(
  'feed/DELETE_FEED_START',
  (data: TDeleteFeedStart) => data
)();
export const deleteFeedSuccess: (
  data: TDeleteFeedStart
) => PayloadAction<string, TDeleteFeedSuccess> = createAction(
  'feed/DELETE_FEED_SUCCESS',
  (data: TDeleteFeedStart) => data
)();
export const deleteFeedFailure: (
  error: IDefaults['errorMessage']
) => PayloadAction<string, IDefaults['errorMessage']> = createAction(
  'feed/DELETE_FEED_FAILURE',
  (error: IDefaults['errorMessage']): IDefaults['errorMessage'] => error
)();
export const deleteFeedReset: EmptyActionCreator<string> = createAction(
  'feed/DELETE_FEED_RESET'
)();
