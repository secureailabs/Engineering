//@ts-nocheck
import {
  all,
  AllEffect,
  call,
  CallEffect,
  put,
  takeLatest,
} from 'redux-saga/effects';

const demo_data = {
  DigitalContracts: {
    uuid1: {
      Title: 'temp',
      VersionNumber: '1',
      ContractStage: 1,
      SubscriptionDays: 7,
      Description: 'test',
      DatasetGuid: '123',
      DatasetName: 'name',
      ActivationTime: 0,
      ExpirationTime: 100,
      Eula: '',
      LegalAgreement: '',
      DataOwnerOrganization: '',
      DOOName: '',
      ResearcherOrganization: '',
      ROName: '',
      LastActivity: 0,
      ProvisioningStatus: 1,
      HostForVirtualMachines: 'localhost',
      NumberOfVCPU: 10,
      Note: '',
    },
  },
};

import {
  // GET ALL
  getAllDigitalContractsFailure,
  getAllDigitalContractsStart,
  getAllDigitalContractsSuccess,
  // GET ONE
  getDigitalContractFailure,
  getDigitalContractStart,
  getDigitalContractSuccess,
  // PATCH ACTIVATE
  patchActivateDigitalContractFailure,
  patchActivateDigitalContractStart,
  patchActivateDigitalContractSuccess,
  // PATCH ACCEPT
  patchAcceptDigitalContractFailure,
  patchAcceptDigitalContractStart,
  patchAcceptDigitalContractSuccess,
  // POST
  postDigitalContractFailure,
  postDigitalContractStart,
  postDigitalContractSuccess,
  // PATCH ASSOCIATE AZURE
  patchAssociateAzureFailure,
  patchAssociateAzureStart,
  patchAssociateAzureSuccess,
  // GET PROVISIONING STATUS
  getProvisioningStatusFailure,
  getProvisioningStatusStart,
  getProvisioningStatusSuccess,
  // POST PROVISION
  provisionDigitalContractFailure,
  provisionDigitalContractStart,
  provisionDigitalContractSuccess,
  // POST
  deprovisionDigitalContractFailure,
  deprovisionDigitalContractStart,
  deprovisionDigitalContractSuccess,
} from './digitalContract.actions';

import {
  getAllDigitalContractsAPI,
  getDigitalContractAPI,
  patchActivateDigitalContractAPI,
  patchAcceptDigitalContractAPI,
  postDigitalContractAPI,
  patchAssociateAzureAPI,
  getProvisioningStatusAPI,
  provisionDigitalContractAPI,
  deprovisionDigitalContractAPI,
} from './digitalContract.apis';

import { AxiosResponse } from 'axios';
import {
  TGetDigitalContractSuccess,
  TGetAllDigitalContractsSuccess,
  TPatchAcceptDigitalContractSuccess,
  TPostDigitalContractSuccess,
  TPostDigitalContractStart,
  TPatchAcceptDigitalContractStart,
  TPatchActivateDigitalContractStart,
  TPatchActivateDigitalContractSuccess,
  TPatchAssociateAzureStart,
  TPatchAssociateAzureSuccess,
  TGetProvisioningStatusStart,
  TGetProvisioningStatusSuccess,
  TProvisionDigitalContractStart,
  TProvisionDigitalContractSuccess,
} from './digitalContract.typeDefs';

// GET PROVISIONING STATUS

export function* getProvisioningStatus({
  payload,
}: ReturnType<typeof getProvisioningStatusStart>) {
  try {
    const { data } = (yield getProvisioningStatusAPI({
      data: payload,
    })) as AxiosResponse<TGetProvisioningStatusSuccess>;
    yield put(getProvisioningStatusSuccess(data));
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(getProvisioningStatusFailure(error));
  }
}

export function* onGetProvisioningStatusStart() {
  yield takeLatest(getProvisioningStatusStart, getProvisioningStatus);
}

// PATCH ASSOCIATE AZURE

export function* patchAssociateAzure({
  payload,
}: ReturnType<typeof patchAssociateAzureStart>) {
  try {
    yield patchAssociateAzureAPI({ data: payload });

    yield put(patchAssociateAzureSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(patchAssociateAzureFailure(error));
  }
}

export function* onPatchAssociateAzureStart() {
  yield takeLatest(patchAssociateAzureStart, patchAssociateAzure);
}

// POST

export function* postDigitalContract({
  payload,
}: ReturnType<typeof postDigitalContractStart>) {
  try {
    yield postDigitalContractAPI({ data: payload });

    yield put(postDigitalContractSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(postDigitalContractFailure(error));
  }
}

export function* onPostDigitalContractStart() {
  yield takeLatest(postDigitalContractStart, postDigitalContract);
}

// PATCH ACTIVATE

export function* patchActivateDigitalContract({
  payload,
}: ReturnType<typeof patchActivateDigitalContractStart>) {
  try {
    yield patchActivateDigitalContractAPI({ data: payload });
    console.log('here');
    yield put(patchActivateDigitalContractSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(patchActivateDigitalContractFailure(error.response.data));
  }
}

export function* onPatchActivateDigitalContractStart() {
  yield takeLatest(
    patchActivateDigitalContractStart,
    patchActivateDigitalContract
  );
}

// PATCH ACCEPT

export function* patchAcceptDigitalContract({
  payload,
}: ReturnType<typeof patchAcceptDigitalContractStart>) {
  try {
    //@ts-ignore
    yield patchAcceptDigitalContractAPI({ data: payload });

    yield put(patchAcceptDigitalContractSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(patchAcceptDigitalContractFailure(error.response.data));
  }
}

export function* onPatchAcceptDigitalContractStart() {
  yield takeLatest(patchAcceptDigitalContractStart, patchAcceptDigitalContract);
}

// GET ALL

export function* getAllDigitalContractsSaga() {
  yield put(getAllDigitalContractsSuccess(demo_data));
  // try {
  //   const {
  //     data,
  //   } = (yield getAllDigitalContractsAPI()) as AxiosResponse<TGetAllDigitalContractsSuccess>;

  //   yield put(getAllDigitalContractsSuccess(data));
  // } catch (err) {
  //   console.log(err);
  //   // tslint:disable-next-line: no-unsafe-any
  //   yield put(getAllDigitalContractsFailure(err.response));
  // }
}

export function* onGetAllDigitalContractsStart() {
  yield takeLatest(getAllDigitalContractsStart, getAllDigitalContractsSaga);
}

// GET ONE

export function* getDigitalContractSaga({
  payload,
}: ReturnType<typeof getDigitalContractStart>) {
  try {
    console.log(payload);
    const { data } = (yield getDigitalContractAPI({
      data: payload,
    })) as AxiosResponse<TGetDigitalContractSuccess>;
    yield put(getDigitalContractSuccess(data));
  } catch (err) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(getDigitalContractFailure(err.response.data));
  }
}

export function* onGetDigitalContractStart() {
  yield takeLatest(getDigitalContractStart, getDigitalContractSaga);
}

// POST PROVISION

export function* provisionDigitalContract({
  payload,
}: ReturnType<typeof provisionDigitalContractStart>) {
  try {
    yield provisionDigitalContractAPI({ data: payload });

    yield put(provisionDigitalContractSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(provisionDigitalContractFailure(error));
  }
}

export function* onProvisionDigitalContractStart() {
  yield takeLatest(provisionDigitalContractStart, provisionDigitalContract);
}

// POST DEPROVISION

export function* deprovisionDigitalContract({
  payload,
}: ReturnType<typeof deprovisionDigitalContractStart>) {
  try {
    yield deprovisionDigitalContractAPI({ data: payload });

    yield put(deprovisionDigitalContractSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(deprovisionDigitalContractFailure(error));
  }
}

export function* onDeprovisionDigitalContractStart() {
  yield takeLatest(deprovisionDigitalContractStart, deprovisionDigitalContract);
}

function* contactSagas(): Generator<AllEffect<CallEffect<void>>, void> {
  yield all([
    call(onGetAllDigitalContractsStart),
    call(onPostDigitalContractStart),
    call(onGetDigitalContractStart),
    call(onPatchAcceptDigitalContractStart),
    call(onPatchActivateDigitalContractStart),
    call(onPatchAssociateAzureStart),
    call(onGetProvisioningStatusStart),
    call(onProvisionDigitalContractStart),
    call(onDeprovisionDigitalContractStart),
  ]);
}

export default contactSagas;
