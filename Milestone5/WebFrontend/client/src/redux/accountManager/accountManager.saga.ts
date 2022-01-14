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
  getAllAccountManagersFailure,
  getAllAccountManagersStart,
  getAllAccountManagersSuccess,
  // GET ONE
  getAccountManagerFailure,
  getAccountManagerStart,
  getAccountManagerSuccess,

  // PUT UPDATE USER
  putUpdateUserFailure,
  putUpdateUserStart,
  putUpdateUserSuccess,

  // PUT UPDATE PASSWORD
  putUpdatePasswordFailure,
  putUpdatePasswordStart,
  putUpdatePasswordSuccess,

  // PUT UPDATE ACCESS RIGHTS
  putUpdateAccessRightsFailure,
  putUpdateAccessRightsStart,
  putUpdateAccessRightsSuccess,

  // POST
  postAccountManagerFailure,
  postAccountManagerStart,
  postAccountManagerSuccess,

  // DELETE
  deleteAccountManagerFailure,
  deleteAccountManagerStart,
  deleteAccountManagerSuccess,

  // PUT
  putAccountManagerFailure,
  putAccountManagerStart,
  putAccountManagerSuccess,
} from './accountManager.actions';

import {
  getAllAccountManagersAPI,
  getAccountManagerAPI,
  putUpdateUserAPI,
  putUpdatePasswordAPI,
  putUpdateAccessRightsAPI,
  postAccountManagerAPI,
  deleteAccountManagerAPI,
  putAccountManagerAPI,
} from './accountManager.apis';

import { AxiosResponse } from 'axios';
import {
  TGetAccountManagerSuccess,
  TGetAllAccountManagersSuccess,
  TPostAccountManagerSuccess,
  TPostAccountManagerStart,
  TPutUpdateUserStart,
  TPutUpdateUserSuccess,
  TPutUpdatePasswordStart,
  TPutUpdatePasswordSuccess,
  TPutUpdateAccessRightsStart,
  TPutUpdateAccessRightsSuccess,
  TDeleteAccountManagerSuccess,
  TGetAllAccountManagersStart,
  TPutAccountManagerStart,
  TPutAccountManagerSuccess,
} from './accountManager.typeDefs';

// POST

export function* postAccountManager({
  payload,
}: ReturnType<typeof postAccountManagerStart>) {
  try {
    yield postAccountManagerAPI({ data: payload });

    yield put(postAccountManagerSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(postAccountManagerFailure(error));
  }
}

export function* onPostAccountManagerStart() {
  yield takeLatest(postAccountManagerStart, postAccountManager);
}

// PUT UPDATE USER

export function* putUpdateUser({
  payload,
}: ReturnType<typeof putUpdateUserStart>) {
  try {
    yield putUpdateUserAPI({ data: payload });
    console.log('here');
    yield put(putUpdateUserSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(putUpdateUserFailure(error?.response?.data));
  }
}

export function* onPutUpdateUserStart() {
  yield takeLatest(putUpdateUserStart, putUpdateUser);
}

// PUT UPDATE PASSWORD

export function* putUpdatePassword({
  payload,
}: ReturnType<typeof putUpdatePasswordStart>) {
  try {
    yield putUpdatePasswordAPI({ data: payload });
    console.log('here');
    yield put(putUpdatePasswordSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(putUpdatePasswordFailure(error?.response?.data));
  }
}

export function* onPutUpdatePasswordStart() {
  yield takeLatest(putUpdatePasswordStart, putUpdatePassword);
}

// PUT UPDATE ACCESS RIGHTS

export function* putUpdateAccessRights({
  payload,
}: ReturnType<typeof putUpdateAccessRightsStart>) {
  try {
    yield putUpdateAccessRightsAPI({ data: payload });
    console.log('here');
    yield put(putUpdateAccessRightsSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(putUpdateAccessRightsFailure(error?.response?.data));
  }
}

export function* onPutUpdateAccessRightsStart() {
  yield takeLatest(putUpdateAccessRightsStart, putUpdateAccessRights);
}

// GET ALL

export function* getAllAccountManagersSaga({
  payload,
}: ReturnType<typeof getAllAccountManagersStart>) {
  try {
    const { data } = (yield getAllAccountManagersAPI({
      data: payload,
    })) as AxiosResponse<TGetAllAccountManagersSuccess>;
    yield put(getAllAccountManagersSuccess(data));
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(getAllAccountManagersFailure(err.response.data));
  }
}

export function* onGetAllAccountManagersStart() {
  yield takeLatest(getAllAccountManagersStart, getAllAccountManagersSaga);
}

// GET ONE

export function* getAccountManagerSaga({
  payload,
}: ReturnType<typeof getAccountManagerStart>) {
  try {
    console.log(payload);
    const { data } = (yield getAccountManagerAPI({
      data: payload,
    })) as AxiosResponse<TGetAccountManagerSuccess>;
    console.log(data);

    yield put(getAccountManagerSuccess(data));
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(getAccountManagerFailure(err.response.data));
  }
}

export function* onGetAccountManagerStart() {
  yield takeLatest(getAccountManagerStart, getAccountManagerSaga);
}

// DELETE

export function* deleteAccountManagerSaga({
  payload,
}: ReturnType<typeof deleteAccountManagerStart>) {
  try {
    const { data } = (yield deleteAccountManagerAPI({
      data: payload,
    })) as AxiosResponse<TDeleteAccountManagerSuccess>;
    yield put(deleteAccountManagerSuccess(data));
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(deleteAccountManagerFailure(err.response.data));
  }
}

export function* onDeleteAccountManagerStart() {
  yield takeLatest(deleteAccountManagerStart, deleteAccountManagerSaga);
}

// PUT (reopen account)

export function* putAccountManagerSaga({
  payload,
}: ReturnType<typeof putAccountManagerStart>) {
  try {
    const { data } = (yield putAccountManagerAPI({
      data: payload,
    })) as AxiosResponse<TPutAccountManagerSuccess>;
    yield put(putAccountManagerSuccess(data));
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(putAccountManagerFailure(err.response.data));
  }
}

export function* onPutAccountManagerStart() {
  yield takeLatest(putAccountManagerStart, putAccountManagerSaga);
}

function* contactSagas(): Generator<AllEffect<CallEffect<void>>, void> {
  yield all([
    call(onGetAllAccountManagersStart),
    call(onPostAccountManagerStart),
    call(onGetAccountManagerStart),
    call(onPutUpdateUserStart),
    call(onPutUpdatePasswordStart),
    call(onPutUpdateAccessRightsStart),
    call(onDeleteAccountManagerStart),
    call(onPutAccountManagerStart),
  ]);
}

export default contactSagas;
