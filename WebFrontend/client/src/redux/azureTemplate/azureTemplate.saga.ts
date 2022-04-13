//@ts-nocheck
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
  postAzureTemplateStart,
  postAzureTemplateSuccess,
  postAzureTemplateFailure,

  // GET ALL
  getAllAzureTemplatesStart,
  getAllAzureTemplatesSuccess,
  getAllAzureTemplatesFailure,

  // GET ONE
  getAzureTemplateStart,
  getAzureTemplateSuccess,
  getAzureTemplateFailure,

  // PUT PUTUPDATE
  putUpdateAzureTemplateStart,
  putUpdateAzureTemplateSuccess,
  putUpdateAzureTemplateFailure,

  // PUT PUTUPDATE SECRET
  putUpdateAzureSecretStart,
  putUpdateAzureSecretSuccess,
  putUpdateAzureSecretFailure,

  // DELETE
  deleteAzureTemplateStart,
  deleteAzureTemplateSuccess,
  deleteAzureTemplateFailure,
  deleteAzureTemplateReset,
} from './azureTemplate.actions';

import {
  postAzureTemplateAPI,
  getAllAzureTemplatesAPI,
  getAzureTemplateAPI,
  putUpdateAzureTemplateAPI,
  deleteAzureTemplateAPI,
} from './azureTemplate.apis';

import { AxiosResponse } from 'axios';
import {
  TGetAllAzureTemplatesSuccess,
  TGetAzureTemplateSuccess,
} from './azureTemplate.typesDefs';

const demo_data = {
  Templates: {
    uuid1: {
      Name: 'Name',
      Description: 'Description',
      SubscriptionID: 'SubscriptionID',
      TenantID: 'TenantID',
      ApplicationID: 'ApplicationID',
      ResourceGroup: 'ResourceGroup',
      VirtualNetwork: 'VirtualNetwork',
      HostRegion: 'HostRegion',
      VirtualMachineImage: 'VirtualMachineImage',
      State: 1,
      Note: 'Note',
    },
  },
};

// POST

export function* postAzureTemplateSaga({
  payload,
}: ReturnType<typeof postAzureTemplateStart>) {
  try {
    yield postAzureTemplateAPI({ data: payload });
    yield put(postAzureTemplateSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(postAzureTemplateFailure(error));
  }
}

export function* onPostAzureTemplateStart() {
  yield takeLatest(postAzureTemplateStart, postAzureTemplateSaga);
}

// GET ALL

export function* getAllAzureTemplatesSaga({}: ReturnType<
  typeof getAllAzureTemplatesStart
>) {
  yield put(getAllAzureTemplatesSuccess(demo_data));
  // try {
  //   const {
  //     data,
  //   } = (yield getAllAzureTemplatesAPI()) as AxiosResponse<TGetAllAzureTemplatesSuccess>;
  //   yield put(getAllAzureTemplatesSuccess(data));
  // } catch (err) {
  //   // tslint:disable-next-line: no-unsafe-any
  //   yield put(getAllAzureTemplatesFailure(err.response.data));
  // }
}

export function* onGetAllAzureTemplatesStart() {
  yield takeLatest(getAllAzureTemplatesStart, getAllAzureTemplatesSaga);
}

// GET ONE

export function* getAzureTemplateSaga({
  payload,
}: ReturnType<typeof getAzureTemplateStart>) {
  try {
    const { data } = (yield getAzureTemplateAPI({
      data: payload,
    })) as AxiosResponse<TGetAzureTemplateSuccess>;
    yield put(getAzureTemplateSuccess(data));
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(getAzureTemplateFailure(err.response.data));
  }
}

export function* onGetAzureTemplateStart() {
  yield takeLatest(getAzureTemplateStart, getAzureTemplateSaga);
}

// PUT PUTUPDATE AZURE TEMPLATE

export function* putUpdateAzureTemplate({
  payload,
}: ReturnType<typeof putUpdateAzureTemplateStart>) {
  try {
    yield putUpdateAzureTemplateAPI({ data: payload });
    yield put(putUpdateAzureTemplateSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(putUpdateAzureTemplateFailure(error?.response?.data));
  }
}

export function* onPutUpdateAzureTemplateStart() {
  yield takeLatest(putUpdateAzureTemplateStart, putUpdateAzureTemplate);
}

// PUT PUTUPDATE AZURE SECRET

export function* putUpdateAzureSecret({
  payload,
}: ReturnType<typeof putUpdateAzureSecretStart>) {
  try {
    yield putUpdateAzureTemplateAPI({ data: payload });
    yield put(putUpdateAzureSecretSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(putUpdateAzureSecretFailure(error?.response?.data));
  }
}

export function* onPutUpdateAzureSecretStart() {
  yield takeLatest(putUpdateAzureSecretStart, putUpdateAzureSecret);
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

function* azureTemplateSagas(): Generator<AllEffect<CallEffect<void>>, void> {
  yield all([
    call(onPostAzureTemplateStart),
    call(onGetAllAzureTemplatesStart),
    call(onGetAzureTemplateStart),
    call(onPutUpdateAzureTemplateStart),
    call(onPutUpdateAzureSecretStart),
    call(onDeleteAzureTemplateStart),
  ]);
}

export default azureTemplateSagas;
