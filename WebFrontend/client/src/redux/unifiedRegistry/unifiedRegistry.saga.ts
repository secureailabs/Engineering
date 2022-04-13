//@ts-nocheck
import {
  all,
  AllEffect,
  call,
  CallEffect,
  put,
  takeLatest,
} from 'redux-saga/effects';

import { demo_data } from './unifiedRegistry.data';

import {
  // GET ALL
  getAllUnifiedRegistriesFailure,
  getAllUnifiedRegistriesStart,
  getAllUnifiedRegistriesSuccess,
  // GET ONE
  getUnifiedRegistryFailure,
  getUnifiedRegistryStart,
  getUnifiedRegistrySuccess,
  // POST
  postUnifiedRegistryFailure,
  postUnifiedRegistryStart,
  postUnifiedRegistrySuccess,
  // DELETE
  deleteUnifiedRegistryFailure,
  deleteUnifiedRegistryStart,
  deleteUnifiedRegistrySuccess,
  // PUT
  putUnifiedRegistryFailure,
  putUnifiedRegistryStart,
  putUnifiedRegistrySuccess,
} from './unifiedRegistry.actions';

import {
  getAllUnifiedRegistriesAPI,
  getUnifiedRegistryAPI,
  postUnifiedRegistryAPI,
  deleteUnifiedRegistryAPI,
  putUnifiedRegistryAPI,
} from './unifiedRegistry.apis';

import { AxiosResponse } from 'axios';
import {
  TGetUnifiedRegistrySuccess,
  TGetAllUnifiedRegistriesSuccess,
  TPostUnifiedRegistrySuccess,
  TPostUnifiedRegistryStart,
  TDeleteUnifiedRegistrySuccess,
  TPutUnifiedRegistryStart,
  TPutUnifiedRegistrySuccess,
} from './unifiedRegistry.types';

// POST

export function* postUnifiedRegistry({
  payload,
}: ReturnType<typeof postUnifiedRegistryStart>) {
  try {
    yield postUnifiedRegistryAPI({ data: payload });

    yield put(postUnifiedRegistrySuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(postUnifiedRegistryFailure(error));
  }
}

export function* onPostUnifiedRegistryStart() {
  yield takeLatest(postUnifiedRegistryStart, postUnifiedRegistry);
}
// GET ALL

export function* getAllUnifiedRegistrysSaga({}: ReturnType<
  typeof getAllUnifiedRegistriesStart
>) {
  yield put(getAllUnifiedRegistriesSuccess(demo_data));
  // try {
  //   const { data } = (yield getAllUnifiedRegistriesAPI(
  //     {}
  //   )) as AxiosResponse<TGetAllUnifiedRegistriesSuccess>;
  //   yield put(getAllUnifiedRegistriesSuccess(data));
  // } catch (err) {
  //   // tslint:disable-next-line: no-unsafe-any
  //   yield put(getAllUnifiedRegistriesFailure(err.response.data));
  // }
}

export function* onGetAllUnifiedRegistriesStart() {
  yield takeLatest(getAllUnifiedRegistriesStart, getAllUnifiedRegistrysSaga);
}

// GET ONE

export function* getUnifiedRegistrySaga({
  payload,
}: ReturnType<typeof getUnifiedRegistryStart>) {
  console.log(payload);
  yield put(
    getUnifiedRegistrySuccess({
      UnifiedRegistry: demo_data.UnifiedRegistries[payload],
    })
  );
  // try {
  //   console.log(payload);
  //   const { data } = (yield getUnifiedRegistryAPI({
  //     data: payload,
  //   })) as AxiosResponse<TGetUnifiedRegistrySuccess>;
  //   console.log(data);

  //   yield put(getUnifiedRegistrySuccess(data));
  // } catch (err) {
  //   // tslint:disable-next-line: no-unsafe-any
  //   yield put(getUnifiedRegistryFailure(err.response.data));
  // }
}

export function* onGetUnifiedRegistryStart() {
  yield takeLatest(getUnifiedRegistryStart, getUnifiedRegistrySaga);
}

// DELETE

export function* deleteUnifiedRegistrySaga({
  payload,
}: ReturnType<typeof deleteUnifiedRegistryStart>) {
  try {
    const { data } = (yield deleteUnifiedRegistryAPI({
      data: payload,
    })) as AxiosResponse<TDeleteUnifiedRegistrySuccess>;
    yield put(deleteUnifiedRegistrySuccess(data));
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(deleteUnifiedRegistryFailure(err.response.data));
  }
}

export function* onDeleteUnifiedRegistryStart() {
  yield takeLatest(deleteUnifiedRegistryStart, deleteUnifiedRegistrySaga);
}

// PUT (reopen account)

export function* putUnifiedRegistrySaga({
  payload,
}: ReturnType<typeof putUnifiedRegistryStart>) {
  try {
    const { data } = (yield putUnifiedRegistryAPI({
      data: payload,
    })) as AxiosResponse<TPutUnifiedRegistrySuccess>;
    yield put(putUnifiedRegistrySuccess());
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(putUnifiedRegistryFailure(err.response.data));
  }
}

export function* onPutUnifiedRegistryStart() {
  yield takeLatest(putUnifiedRegistryStart, putUnifiedRegistrySaga);
}

function* contactSagas(): Generator<AllEffect<CallEffect<void>>, void> {
  yield all([
    call(onGetAllUnifiedRegistriesStart),
    call(onPostUnifiedRegistryStart),
    call(onGetUnifiedRegistryStart),
    call(onDeleteUnifiedRegistryStart),
    call(onPutUnifiedRegistryStart),
  ]);
}

export default contactSagas;
