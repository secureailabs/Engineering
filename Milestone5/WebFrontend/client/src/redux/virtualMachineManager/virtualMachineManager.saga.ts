import {
  all,
  AllEffect,
  call,
  CallEffect,
  put,
  takeLatest,
} from 'redux-saga/effects';

const demo_data = {
  uuid1: {
    HostForVirtualMachines: 'Researcher',
    ResearcherOrganization: 'Hopsital 1',
    DataOwnerOrganization: 'Org1',
    VirtualMachinesAssociatedWithDc: {
      uuid: {
        VirtualMachineGuid: 'uuid2',
        DigitalContractGuid: 'guid',
        DigitalContractTitle: 'Digi',
        DigitalContract: {
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
        State: 4,
        RegistrationTime: 20,
        HeartbeatBroadcastTime: 10,
        IPAddress: '127.0.0.1',
        NumberOfVCPU: 10,
        HostRegion: 'East',
        StartTime: 1200,
        Note: '',
      },
    },
  },
};

import { getDigitalContractAPI } from '../digitalContract/digitalContract.apis';

import {
  // GET ONE
  getVirtualMachineFailure,
  getVirtualMachineStart,
  getVirtualMachineSuccess,

  // GET ALL
  getAllVirtualMachinesFailure,
  getAllVirtualMachinesStart,
  getAllVirtualMachinesSuccess,
  // PUT
  putVirtualMachineFailure,
  putVirtualMachineStart,
  putVirtualMachineSuccess,
} from './virtualMachineManager.actions';

import {
  getVirtualMachineAPI,
  putVirtualMachineAPI,
  getAllVirtualMachinesAPI,
} from './virtualMachineManager.apis';

import { AxiosResponse } from 'axios';
import {
  TGetVirtualMachineSuccess,
  TPutVirtualMachineStart,
  TPutVirtualMachineSuccess,
  TGetAllVirtualMachinesSuccess,
} from './virtualMachineManager.typeDefs';

// PUT

export function* putVirtualMachine({
  payload,
}: ReturnType<typeof putVirtualMachineStart>) {
  try {
    yield putVirtualMachineAPI({ data: payload });
    console.log('here');
    yield put(putVirtualMachineSuccess());
  } catch (error) {
    // tslint:disable-next-line: no-unsafe-any
    yield put(putVirtualMachineFailure(error.response.data));
  }
}

export function* onPutVirtualMachineStart() {
  yield takeLatest(putVirtualMachineStart, putVirtualMachine);
}

// GET ONE

export function* getVirtualMachineSaga({
  payload,
}: ReturnType<typeof getVirtualMachineStart>) {
  try {
    const { data } = yield (getVirtualMachineAPI({
      data: payload,
    }) as unknown) as AxiosResponse<{
      data: { VirtualMachine: TGetVirtualMachineSuccess };
    }> | null;
    console.log('VIRTUAL MACHINE DATA: ', data);
    //@ts-ignore

    //@ts-ignore
    const digitalContract = yield getDigitalContractAPI({
      //@ts-ignore
      data: {
        DigitalContractGuid: data['VirtualMachine'].DigitalContractGuid,
      },
    });
    data['VirtualMachine']['DigitalContract'] = digitalContract.data;

    yield put(getVirtualMachineSuccess(data['VirtualMachine']));
  } catch (err) {
    console.log('ERROR: ', err);
    // tslint:disable-next-line: no-unsafe-any
    yield put(getVirtualMachineFailure(err.response.data));
  }
}

export function* onGetVirtualMachineStart() {
  yield takeLatest(getVirtualMachineStart, getVirtualMachineSaga);
}

// GET ALL

export function* getAllVirtualMachinesSaga() {
  yield put(getAllVirtualMachinesSuccess(demo_data));
  // try {
  //   const {
  //     data,
  //   } = yield (getAllVirtualMachinesAPI() as unknown) as AxiosResponse<{
  //     data: { VirtualMachines: TGetAllVirtualMachinesSuccess };
  //   }> | null;
  //   console.log('DATA: ', data['VirtualMachines']);
  //   for (const [key, value] of Object.entries(data['VirtualMachines'])) {
  //     //@ts-ignore
  //     const digitalContract = yield getDigitalContractAPI({
  //       data: { DigitalContractGuid: key },
  //     });
  //     for (const [key2, value2] of Object.entries(
  //       //@ts-ignore
  //       value.VirtualMachinesAssociatedWithDc
  //     )) {
  //       // //@ts-ignore
  //       // const digitalContract = yield getDigitalContractAPI({
  //       //   //@ts-ignore
  //       //   data: { DigitalContractGuid: value2.DigitalContractGuid },
  //       // });
  //       data['VirtualMachines'][key].VirtualMachinesAssociatedWithDc[key2][
  //         'DigitalContract'
  //       ] = digitalContract.data;
  //     }
  //   }

  //   yield put(getAllVirtualMachinesSuccess(data['VirtualMachines']));
  // } catch (err) {
  //   // tslint:disable-next-line: no-unsafe-any
  //   yield put(getAllVirtualMachinesFailure(err.response.data));
  // }
}

export function* onGetAllVirtualMachinesStart() {
  yield takeLatest(getAllVirtualMachinesStart, getAllVirtualMachinesSaga);
}

function* virtualMachineManagerSagas(): Generator<
  AllEffect<CallEffect<void>>,
  void
> {
  yield all([
    call(onGetVirtualMachineStart),
    call(onPutVirtualMachineStart),
    call(onGetAllVirtualMachinesStart),
  ]);
}

export default virtualMachineManagerSagas;
