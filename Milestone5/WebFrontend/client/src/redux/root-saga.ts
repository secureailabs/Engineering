// calls all sagas

import { call, all } from 'redux-saga/effects';
import userSagas from './user/user.saga';
import digitalContractSagas from './digitalContract/digitalContract.saga';
import datasetSagas from './dataset/dataset.saga';
import accountManagerSagas from './accountManager/accountManager.saga';
import organizationSagas from './organization/organization.saga';
import azureTemplateSagas from './azureTemplate/azureTemplate.saga';
import virtualMachineManagerSagas from './virtualMachineManager/virtualMachineManager.saga';
import feedSagas from './feed/feed.saga';
import unifiedRegistrySagas from './unifiedRegistry/unifiedRegistry.saga';
export default function* rootSaga() {
  yield all([
    call(userSagas),
    call(feedSagas),
    call(digitalContractSagas),
    call(datasetSagas),
    call(accountManagerSagas),
    call(organizationSagas),
    call(azureTemplateSagas),
    call(unifiedRegistrySagas),
    call(virtualMachineManagerSagas),
  ]);
}
