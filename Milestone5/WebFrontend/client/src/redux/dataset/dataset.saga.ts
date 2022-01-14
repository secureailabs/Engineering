import {
  all,
  AllEffect,
  call,
  CallEffect,
  put,
  takeLatest,
} from 'redux-saga/effects';

import {
  // GET ALL
  getAllDatasetsFailure,
  getAllDatasetsStart,
  getAllDatasetsSuccess,
  // GET ONE
  getDatasetFailure,
  getDatasetStart,
  getDatasetSuccess,
  // POST
  postDatasetFailure,
  postDatasetStart,
  postDatasetSuccess,
} from './dataset.actions';

import {
  getAllDatasetsAPI,
  getDatasetAPI,
  postDatasetAPI,
} from './dataset.apis';

import { AxiosResponse } from 'axios';
import {
  TGetDatasetSuccess,
  TGetAllDatasetsSuccess,
  TPostDatasetSuccess,
  TPostDatasetStart,
} from './dataset.typeDefs';

// POST

export function* postDataset({ payload }: ReturnType<typeof postDatasetStart>) {
  try {
    yield postDatasetAPI({ data: payload });

    yield put(postDatasetSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(postDatasetFailure(error.response.data));
  }
}

export function* onPostDatasetStart() {
  yield takeLatest(postDatasetStart, postDataset);
}

// GET ALL

export function* getAllDatasetsSaga() {
  try {
    const {
      data,
    } = (yield getAllDatasetsAPI()) as AxiosResponse<TGetAllDatasetsSuccess>;
    yield put(getAllDatasetsSuccess(data));
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(getAllDatasetsFailure(err.response.data));
  }
}

export function* onGetAllDatasetsStart() {
  yield takeLatest(getAllDatasetsStart, getAllDatasetsSaga);
}

// GET ONE

export function* getDatasetSaga({
  payload,
}: ReturnType<typeof getDatasetStart>) {
  try {
    const { data } = (yield getDatasetAPI({
      data: payload,
    })) as AxiosResponse<TGetDatasetSuccess>;
    yield put(getDatasetSuccess(data));
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(getDatasetFailure(err.response.data));
  }
}

export function* onGetDatasetStart() {
  yield takeLatest(getDatasetStart, getDatasetSaga);
}

function* contactSagas(): Generator<AllEffect<CallEffect<void>>, void> {
  yield all([
    call(onGetAllDatasetsStart),
    call(onPostDatasetStart),
    call(onGetDatasetStart),
  ]);
}

export default contactSagas;
