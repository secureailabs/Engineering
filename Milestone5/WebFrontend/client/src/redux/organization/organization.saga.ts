import {
  all,
  AllEffect,
  call,
  CallEffect,
  put,
  takeLatest,
} from 'redux-saga/effects';

import {
  // GET ONE
  getOrganizationFailure,
  getOrganizationStart,
  getOrganizationSuccess,
  // PUT
  putOrganizationFailure,
  putOrganizationStart,
  putOrganizationSuccess,
} from './organization.actions';

import { getOrganizationAPI, putOrganizationAPI } from './organization.apis';

import { AxiosResponse } from 'axios';
import {
  TGetOrganizationSuccess,
  TPutOrganizationStart,
  TPutOrganizationSuccess,
} from './organization.typeDefs';

// PUT

export function* putOrganization({
  payload,
}: ReturnType<typeof putOrganizationStart>) {
  try {
    yield putOrganizationAPI({ data: payload });
    console.log('here');
    yield put(putOrganizationSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(putOrganizationFailure(error.response.data));
  }
}

export function* onPutOrganizationStart() {
  yield takeLatest(putOrganizationStart, putOrganization);
}

// GET ONE

export function* getOrganizationSaga() {
  try {
    const { data } = yield (getOrganizationAPI() as unknown) as AxiosResponse<{
      data: { OrganizationInformation: TGetOrganizationSuccess };
    }> | null;
    console.log(data);

    yield put(getOrganizationSuccess(data['OrganizationInformation']));
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(getOrganizationFailure(err.response.data));
  }
}

export function* onGetOrganizationStart() {
  yield takeLatest(getOrganizationStart, getOrganizationSaga);
}

function* organizationSagas(): Generator<AllEffect<CallEffect<void>>, void> {
  yield all([call(onGetOrganizationStart), call(onPutOrganizationStart)]);
}

export default organizationSagas;
