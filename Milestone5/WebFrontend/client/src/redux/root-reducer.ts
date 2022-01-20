import { combineReducers } from 'redux';
import { persistReducer, WebStorage } from 'redux-persist';
import localStorage from 'redux-persist/lib/storage';
import { IEventState } from './audit-log-manager/audit-log-manager.reducer';
import { IDigitalContractState } from './digitalContract/digitalContract.reducer';
import { IDatasetState } from './dataset/dataset.reducer';
import { IAccountManagerState } from './accountManager/accountManager.reducer';
import { IOrganizationState } from './organization/organization.reducer';
import { IVirtualMachineState } from './virtualMachineManager/virtualMachineManager.reducer';
import { IAzureTemplatesManagerState } from './azureTemplatesManager/azureTemplatesManager.reducer';

// import userReducer from './user/user.reducer';
import userReducer, { IUserState } from './user/user.reducer';
import digitalContractReducer from './digitalContract/digitalContract.reducer';
import datasetReducer from './dataset/dataset.reducer';
import accountManagerReducer from './accountManager/accountManager.reducer';
import organizationReducer from './organization/organization.reducer';
import virtualMachineManagerReducer from './virtualMachineManager/virtualMachineManager.reducer';
import azureTemplatesReducer from './azureTemplatesManager/azureTemplatesManager.reducer';

export interface IState {
  user: IUserState;
  'audit-log-manager': IEventState;
  digitalContract: IDigitalContractState;
  dataset: IDatasetState;
  accountManager: IAccountManagerState;
  organization: IOrganizationState;
  virtualMachineManager: IVirtualMachineState;
  azureTemplatesManager: IAzureTemplatesManagerState;
}

const persistConfig: {
  key: string;
  storage: WebStorage;
  whitelist: never[];
} = {
  key: 'root',
  storage: localStorage,
  whitelist: [],
  // Whitelist allows us to save redux state after reload
};

const rootReducer = combineReducers({
  user: userReducer,
  digitalContract: digitalContractReducer,
  dataset: datasetReducer,
  accountManager: accountManagerReducer,
  organization: organizationReducer,
  virtualMachineManager: virtualMachineManagerReducer,
  azureTemplatesManager: azureTemplatesReducer,
});

export default persistReducer(persistConfig, rootReducer);
