import {
  all,
  AllEffect,
  call,
  CallEffect,
  put,
  takeLatest,
} from 'redux-saga/effects';

import {
  getAllEventsFailure,
  getAllEventsStart,
  getAllEventsSuccess,
  postLeafEventsFailure,
  postLeafEventsStart,
  postLeafEventsSuccess,
} from './audit-log-manager.actions';

import { getAllEventsAPI, postLeafEventsAPI } from './audit-log-manager.apis';

import { AxiosResponse } from 'axios';
import { IGetAllEventsSuccess } from './audit-log-manager.typeDefs';

// POST

export function* postLeafEvents({
  payload,
}: ReturnType<typeof postLeafEventsStart>) {
  try {
    yield postLeafEventsAPI({ data: payload });

    yield put(postLeafEventsSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(postLeafEventsFailure(error.response.data));
  }
}

export function* onPostEventsStart() {
  yield takeLatest(postLeafEventsStart, postLeafEvents);
}

// GET ALL

export function* getAllEventsSaga() {
  try {
    const {
      data: {
        data: { doc },
      },
    } = (yield getAllEventsAPI()) as AxiosResponse<{
      data: { doc: IGetAllEventsSuccess };
    }>;
    yield put(getAllEventsSuccess());
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(getAllEventsFailure(err.response.data));
  }
}

export function* onGetAllEventsStart() {
  yield takeLatest(getAllEventsStart, getAllEventsSaga);
}

function* contactSagas(): Generator<AllEffect<CallEffect<void>>, void> {
  yield all([call(onGetAllEventsStart), call(onPostEventsStart)]);
}

export default contactSagas;
