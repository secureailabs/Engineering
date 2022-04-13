// tslint:disable: no-null-null-union
import { createReducer } from 'typesafe-actions';

import {
  // GET ALL
  getAllFeedsFailure,
  getAllFeedsReset,
  getAllFeedsStart,
  getAllFeedsSuccess,
  // GET ONE
  getFeedFailure,
  getFeedReset,
  getFeedStart,
  getFeedSuccess,
  // POST
  postFeedFailure,
  postFeedReset,
  postFeedStart,
  postFeedSuccess,

  // DELETE
  deleteFeedFailure,
  deleteFeedReset,
  deleteFeedStart,
  deleteFeedSuccess,

  // PUT (reopen account)
  putFeedFailure,
  putFeedReset,
  putFeedStart,
  putFeedSuccess,
} from './feed.actions';

import type {
  TPostFeedSuccess,
  TGetAllFeedsSuccess,
  TGetFeedSuccess,
  TDeleteFeedSuccess,
  TPutFeedSuccess,
} from './feed.types';

import { IDefaults } from '@redux/typedefs';

export interface IFeedState {
  // GET ALL
  getAllFeedsData: null | TGetAllFeedsSuccess;
  getAllFeedsError: IDefaults['errorMessage'];
  getAllFeedsState: IDefaults['state'];

  // GET ONE
  getFeedData: null | TGetFeedSuccess;
  getFeedError: IDefaults['errorMessage'];
  getFeedState: IDefaults['state'];
  // POST
  postFeedData: null | TPostFeedSuccess;
  postFeedError: IDefaults['errorMessage'];
  postFeedState: IDefaults['state'];

  // DELETE
  deleteFeedData: null | TDeleteFeedSuccess;
  deleteFeedError: IDefaults['errorMessage'];
  deleteFeedState: IDefaults['state'];

  // PUT (reopen account)
  putFeedData: null | TPutFeedSuccess;
  putFeedError: IDefaults['errorMessage'];
  putFeedState: IDefaults['state'];
}

const INITIAL_STATE: IFeedState = {
  // GET ALL
  getAllFeedsData: null,
  getAllFeedsError: null,
  getAllFeedsState: null,

  // GET ONE
  getFeedData: null,
  getFeedError: null,
  getFeedState: null,
  // POST
  postFeedData: null,
  postFeedError: null,
  postFeedState: null,

  // DELETE
  deleteFeedData: null,
  deleteFeedError: null,
  deleteFeedState: null,

  // PUT (reopen account)
  putFeedData: null,
  putFeedError: null,
  putFeedState: null,
};

// tslint:disable-next-line: no-unsafe-any tslint:disable-next-line: typedef
const FeedReducer = createReducer(INITIAL_STATE)
  // POST

  .handleAction(
    postFeedStart,
    (state: IFeedState): IFeedState => ({
      ...state,
      postFeedData: null,
      postFeedError: null,
      postFeedState: 'isLoading',
    })
  )
  .handleAction(
    postFeedSuccess,
    (state: IFeedState, action: { payload: TPostFeedSuccess }): IFeedState => ({
      ...state,
      postFeedData: action.payload,
      postFeedError: null,
      postFeedState: 'success',
    })
  )
  .handleAction(
    postFeedFailure,
    (
      state: IFeedState,
      action: { payload: IDefaults['errorMessage'] }
    ): IFeedState => ({
      ...state,
      postFeedData: null,
      postFeedError: action.payload,
      postFeedState: 'failure',
    })
  )
  .handleAction(
    postFeedReset,
    (state: IFeedState): IFeedState => ({
      ...state,
      postFeedData: null,
      postFeedError: null,
      postFeedState: null,
    })
  )

  // GET ALL

  .handleAction(
    getAllFeedsStart,
    (state: IFeedState): IFeedState => ({
      ...state,
      getAllFeedsData: null,
      getAllFeedsError: null,
      getAllFeedsState: 'isLoading',
    })
  )
  .handleAction(
    getAllFeedsSuccess,
    (
      state: IFeedState,
      action: { payload: TGetAllFeedsSuccess }
    ): IFeedState => ({
      ...state,
      getAllFeedsData: action.payload,
      getAllFeedsError: null,
      getAllFeedsState: 'success',
    })
  )
  .handleAction(
    getAllFeedsFailure,
    (
      state: IFeedState,
      action: { payload: IDefaults['errorMessage'] }
    ): IFeedState => ({
      ...state,
      getAllFeedsData: null,
      getAllFeedsError: action.payload,
      getAllFeedsState: 'failure',
    })
  )
  .handleAction(
    getAllFeedsReset,
    (state: IFeedState): IFeedState => ({
      ...state,
      getAllFeedsData: null,
      getAllFeedsError: null,
      getAllFeedsState: null,
    })
  )

  // GET ONE

  .handleAction(
    getFeedStart,
    (state: IFeedState): IFeedState => ({
      ...state,
      getFeedData: null,
      getFeedError: null,
      getFeedState: 'isLoading',
    })
  )
  .handleAction(
    getFeedSuccess,
    (state: IFeedState, action: { payload: TGetFeedSuccess }): IFeedState => ({
      ...state,
      getFeedData: action.payload,
      getFeedError: null,
      getFeedState: 'success',
    })
  )
  .handleAction(
    getFeedFailure,
    (
      state: IFeedState,
      action: { payload: IDefaults['errorMessage'] }
    ): IFeedState => ({
      ...state,
      getFeedData: null,
      getFeedError: action.payload,
      getFeedState: 'failure',
    })
  )
  .handleAction(
    getFeedReset,
    (state: IFeedState): IFeedState => ({
      ...state,
      getFeedData: null,
      getFeedError: null,
      getFeedState: null,
    })
  )
  // DELETE

  .handleAction(
    deleteFeedStart,
    (state: IFeedState): IFeedState => ({
      ...state,
      deleteFeedData: null,
      deleteFeedError: null,
      deleteFeedState: 'isLoading',
    })
  )
  .handleAction(
    deleteFeedSuccess,
    (
      state: IFeedState,
      action: { payload: TDeleteFeedSuccess }
    ): IFeedState => ({
      ...state,
      deleteFeedData: action.payload,
      deleteFeedError: null,
      deleteFeedState: 'success',
    })
  )
  .handleAction(
    deleteFeedFailure,
    (
      state: IFeedState,
      action: { payload: IDefaults['errorMessage'] }
    ): IFeedState => ({
      ...state,
      deleteFeedData: null,
      deleteFeedError: action.payload,
      deleteFeedState: 'failure',
    })
  )
  .handleAction(
    deleteFeedReset,
    (state: IFeedState): IFeedState => ({
      ...state,
      deleteFeedData: null,
      deleteFeedError: null,
      deleteFeedState: null,
    })
  )

  // PUT (reopen account)

  .handleAction(
    putFeedStart,
    (state: IFeedState): IFeedState => ({
      ...state,
      putFeedData: null,
      putFeedError: null,
      putFeedState: 'isLoading',
    })
  )
  .handleAction(
    putFeedSuccess,
    (state: IFeedState, action: { payload: TPutFeedSuccess }): IFeedState => ({
      ...state,
      putFeedData: action.payload,
      putFeedError: null,
      putFeedState: 'success',
    })
  )
  .handleAction(
    putFeedFailure,
    (
      state: IFeedState,
      action: { payload: IDefaults['errorMessage'] }
    ): IFeedState => ({
      ...state,
      putFeedData: null,
      putFeedError: action.payload,
      putFeedState: 'failure',
    })
  )
  .handleAction(
    putFeedReset,
    (state: IFeedState): IFeedState => ({
      ...state,
      putFeedData: null,
      putFeedError: null,
      putFeedState: null,
    })
  );

export default FeedReducer;
