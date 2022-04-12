// calls all sagas

import { call, all } from 'redux-saga/effects';
import userSagas from './user/user.saga';
import digitalContractSagas from './digitalContract/digitalContract.saga';
import datasetSagas from './dataset/dataset.saga';
import accountManagerSagas from './accountManager/accountManager.saga';
import organizationSagas from './organization/organization.saga';
import azureTemplatesManagerSaga from './azureTemplatesManager/azureTemplatesManager.saga';
import virtualMachineManagerSagas from './virtualMachineManager/virtualMachineManager.saga';
export default function* rootSaga() {
  yield all([
    call(userSagas),
    call(digitalContractSagas),
    call(datasetSagas),
    call(accountManagerSagas),
    call(organizationSagas),
    call(azureTemplatesManagerSaga),
    call(virtualMachineManagerSagas),
  ]);
}
