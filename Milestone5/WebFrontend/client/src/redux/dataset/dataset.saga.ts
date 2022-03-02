//@ts-nocheck
import {
  all,
  AllEffect,
  call,
  CallEffect,
  put,
  takeLatest,
} from 'redux-saga/effects';

import _ from 'lodash';

import {
  // GET ALL
  getAllDatasetsFailure,
  getAllDatasetsStart,
  getAllDatasetsSuccess,
  // GET ONE
  getDatasetFailure,
  getDatasetStart,
  getDatasetSuccess,
  // GET ONE
  getDatasetVersionFailure,
  getDatasetVersionStart,
  getDatasetVersionSuccess,
  // POST
  postDatasetFailure,
  postDatasetStart,
  postDatasetSuccess,
} from './dataset.actions';

import { demo_data } from './dataset.data';

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
  yield put(getAllDatasetsSuccess(demo_data));
  // try {
  //   const {
  //     data,
  //   } = (yield getAllDatasetsAPI()) as AxiosResponse<TGetAllDatasetsSuccess>;
  //   yield put(getAllDatasetsSuccess(data));
  // } catch (err) {
  //   // tslint:disable-next-line: no-unsafe-any
  //   yield put(getAllDatasetsFailure(err.response.data));
  // }
}

export function* onGetAllDatasetsStart() {
  yield takeLatest(getAllDatasetsStart, getAllDatasetsSaga);
}

// GET ONE

export function* getDatasetSaga({
  payload,
}: ReturnType<typeof getDatasetStart>) {
  yield put(
    getDatasetSuccess({ Dataset: demo_data.Datasets[payload.DatasetGuid] })
  );
  // try {
  //   const { data } = (yield getDatasetAPI({
  //     data: payload,
  //   })) as AxiosResponse<TGetDatasetSuccess>;
  //   yield put(getDatasetSuccess(data));
  // } catch (err) {
  //   // tslint:disable-next-line: no-unsafe-any
  //   yield put(getDatasetFailure(err.response.data));
  // }
}

export function* onGetDatasetStart() {
  yield takeLatest(getDatasetStart, getDatasetSaga);
}

// GET VERSION

export function* getDatasetVersionSaga({
  payload,
}: ReturnType<typeof getDatasetVersionStart>) {
  yield put(
    getDatasetVersionSuccess({
      Dataset:
        demo_data.Datasets[payload.DatasetGuid].Versions[payload.Version],
    })
  );
  // try {
  //   const { data } = (yield getDatasetAPI({
  //     data: payload,
  //   })) as AxiosResponse<TGetDatasetSuccess>;
  //   yield put(getDatasetSuccess(data));
  // } catch (err) {
  //   // tslint:disable-next-line: no-unsafe-any
  //   yield put(getDatasetFailure(err.response.data));
  // }
}

export function* onGetDatasetVersionStart() {
  yield takeLatest(getDatasetVersionStart, getDatasetVersionSaga);
}

function* contactSagas(): Generator<AllEffect<CallEffect<void>>, void> {
  yield all([
    call(onGetAllDatasetsStart),
    call(onPostDatasetStart),
    call(onGetDatasetVersionStart),
    call(onGetDatasetStart),
  ]);
}

export default contactSagas;
