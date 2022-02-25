import {
  all,
  AllEffect,
  call,
  CallEffect,
  put,
  takeLatest,
} from 'redux-saga/effects';

import { demo_data } from './feed.data';

import {
  // GET ALL
  getAllFeedsFailure,
  getAllFeedsStart,
  getAllFeedsSuccess,
  // GET ONE
  getFeedFailure,
  getFeedStart,
  getFeedSuccess,
  // POST
  postFeedFailure,
  postFeedStart,
  postFeedSuccess,
  // DELETE
  deleteFeedFailure,
  deleteFeedStart,
  deleteFeedSuccess,
  // PUT
  putFeedFailure,
  putFeedStart,
  putFeedSuccess,
} from './feed.actions';

import {
  getAllFeedsAPI,
  getFeedAPI,
  postFeedAPI,
  deleteFeedAPI,
  putFeedAPI,
} from './feed.apis';

import { AxiosResponse } from 'axios';
import {
  TGetFeedSuccess,
  TGetAllFeedsSuccess,
  TPostFeedSuccess,
  TPostFeedStart,
  TDeleteFeedSuccess,
  TGetAllFeedsStart,
  TPutFeedStart,
  TPutFeedSuccess,
} from './feed.types';

// POST

export function* postFeed({ payload }: ReturnType<typeof postFeedStart>) {
  try {
    yield postFeedAPI({ data: payload });

    yield put(postFeedSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(postFeedFailure(error));
  }
}

export function* onPostFeedStart() {
  yield takeLatest(postFeedStart, postFeed);
}
// GET ALL

export function* getAllFeedsSaga({}: ReturnType<typeof getAllFeedsStart>) {
  yield put(getAllFeedsSuccess(demo_data));
}

export function* onGetAllFeedsStart() {
  yield takeLatest(getAllFeedsStart, getAllFeedsSaga);
}

// GET ONE

export function* getFeedSaga({ payload }: ReturnType<typeof getFeedStart>) {
  try {
    console.log(payload);
    const { data } = (yield getFeedAPI({
      data: payload,
    })) as AxiosResponse<TGetFeedSuccess>;
    console.log(data);

    yield put(getFeedSuccess(data));
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(getFeedFailure(err.response.data));
  }
}

export function* onGetFeedStart() {
  yield takeLatest(getFeedStart, getFeedSaga);
}

// DELETE

export function* deleteFeedSaga({
  payload,
}: ReturnType<typeof deleteFeedStart>) {
  try {
    const { data } = (yield deleteFeedAPI({
      data: payload,
    })) as AxiosResponse<TDeleteFeedSuccess>;
    yield put(deleteFeedSuccess(data));
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(deleteFeedFailure(err.response.data));
  }
}

export function* onDeleteFeedStart() {
  yield takeLatest(deleteFeedStart, deleteFeedSaga);
}

// PUT (reopen account)

export function* putFeedSaga({ payload }: ReturnType<typeof putFeedStart>) {
  try {
    const { data } = (yield putFeedAPI({
      data: payload,
    })) as AxiosResponse<TPutFeedSuccess>;
    yield put(putFeedSuccess());
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(putFeedFailure(err.response.data));
  }
}

export function* onPutFeedStart() {
  yield takeLatest(putFeedStart, putFeedSaga);
}

function* contactSagas(): Generator<AllEffect<CallEffect<void>>, void> {
  yield all([
    call(onGetAllFeedsStart),
    call(onPostFeedStart),
    call(onGetFeedStart),
    call(onDeleteFeedStart),
    call(onPutFeedStart),
  ]);
}

export default contactSagas;
