import {
  all,
  AllEffect,
  call,
  CallEffect,
  put,
  takeLatest,
} from 'redux-saga/effects';

import {
  // POST
  registerAzureTemplateStart,
  registerAzureTemplateSuccess,
  registerAzureTemplateFailure,

  // GET ALL
  listAzureTemplatesStart,
  listAzureTemplatesSuccess,
  listAzureTemplatesFailure,

  // GET ONE
  pullAzureTemplateStart,
  pullAzureTemplateSuccess,
  pullAzureTemplateFailure,

  // PUT UPDATE
  updateAzureTemplateStart,
  updateAzureTemplateSuccess,
  updateAzureTemplateFailure,

  // PUT UPDATE SECRET
  updateAzureSecretStart,
  updateAzureSecretSuccess,
  updateAzureSecretFailure,

  // DELETE
  deleteAzureTemplateStart,
  deleteAzureTemplateSuccess,
  deleteAzureTemplateFailure,
  deleteAzureTemplateReset,
} from './azureTemplatesManager.actions';

import {
  registerAzureTemplateAPI,
  listAzureTemplatesAPI,
  pullAzureTemplateAPI,
  updateAzureTemplateAPI,
  deleteAzureTemplateAPI,
} from './azureTemplatesManager.apis';

import { AxiosResponse } from 'axios';
import {
  TListAzureTemplatesSuccess,
  TPullAzureTemplateSuccess,
} from './azureTemplatesManager.typesDefs';

// POST

export function* registerAzureTemplateSaga({
  payload,
}: ReturnType<typeof registerAzureTemplateStart>) {
  try {
    yield registerAzureTemplateAPI({ data: payload });
    yield put(registerAzureTemplateSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(registerAzureTemplateFailure(error));
  }
}

export function* onRegisterAzureTemplateStart() {
  yield takeLatest(registerAzureTemplateStart, registerAzureTemplateSaga);
}

// GET ALL

export function* listAzureTemplatesSaga({
}: ReturnType<typeof listAzureTemplatesStart>) {
  try {
    const { data } = (yield listAzureTemplatesAPI(
)) as AxiosResponse<TListAzureTemplatesSuccess>;
    yield put(listAzureTemplatesSuccess(data));
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(listAzureTemplatesFailure(err.response.data));
  }
}

export function* onListAzureTemplatesStart() {
  yield takeLatest(listAzureTemplatesStart, listAzureTemplatesSaga);
}

// GET ONE

export function* pullAzureTemplateSaga({
  payload,
}: ReturnType<typeof pullAzureTemplateStart>) {
  try {
    console.log(payload);
    const { data } = (yield pullAzureTemplateAPI({
      data: payload,
    })) as AxiosResponse<TPullAzureTemplateSuccess>;
    console.log(data);

    yield put(pullAzureTemplateSuccess(data));
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(pullAzureTemplateFailure(err.response.data));
  }
}

export function* onPullAzureTemplateStart() {
  yield takeLatest(pullAzureTemplateStart, pullAzureTemplateSaga);
}

// PUT UPDATE AZURE TEMPLATE

export function* updateAzureTemplate({
  payload,
}: ReturnType<typeof updateAzureTemplateStart>) {
  try {
    yield updateAzureTemplateAPI({ data: payload });
    yield put(updateAzureTemplateSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(updateAzureTemplateFailure(error?.response?.data));
  }
}

export function* onUpdateAzureTemplateStart() {
  yield takeLatest(updateAzureTemplateStart, updateAzureTemplate);
}

// PUT UPDATE AZURE SECRET

export function* updateAzureSecret({
  payload,
}: ReturnType<typeof updateAzureSecretStart>) {
  try {
    yield updateAzureTemplateAPI({ data: payload });
    yield put(updateAzureSecretSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(updateAzureSecretFailure(error?.response?.data));
  }
}

export function* onUpdateAzureSecretStart() {
  yield takeLatest(updateAzureSecretStart, updateAzureSecret);
}

// DELETE

export function* deleteAzureTemplateSaga({
  payload,
}: ReturnType<typeof deleteAzureTemplateStart>) {
  try {
    yield deleteAzureTemplateAPI({ data: payload });
    yield put(deleteAzureTemplateSuccess());
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(deleteAzureTemplateFailure(err.response.data));
  }
}

export function* onDeleteAzureTemplateStart() {
  yield takeLatest(deleteAzureTemplateStart, deleteAzureTemplateSaga);
}


function* contactSagas(): Generator<AllEffect<CallEffect<void>>, void> {
  yield all([
    call(onRegisterAzureTemplateStart),
    call(onListAzureTemplatesStart),
    call(onPullAzureTemplateStart),
    call(onUpdateAzureTemplateStart),
    call(onUpdateAzureSecretStart),
    call(onDeleteAzureTemplateStart),
  ]);
}

export default contactSagas;
