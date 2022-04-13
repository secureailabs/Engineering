import { combineReducers } from 'redux';
import { persistReducer, WebStorage } from 'redux-persist';
import localStorage from 'redux-persist/lib/storage';
import { IEventState } from './audit-log-manager/audit-log-manager.reducer';
import { IDigitalContractState } from './digitalContract/digitalContract.reducer';
import { IDatasetState } from './dataset/dataset.reducer';
import { IAccountManagerState } from './accountManager/accountManager.reducer';
import { IOrganizationState } from './organization/organization.reducer';
import { IVirtualMachineState } from './virtualMachineManager/virtualMachineManager.reducer';
import { IAzureTemplateState } from './azureTemplate/azureTemplate.reducer';
import { IFeedState } from './feed/feed.reducer';
import { IUnifiedRegistryState } from './unifiedRegistry/unifiedRegistry.reducer';

// import userReducer from './user/user.reducer';
import userReducer, { IUserState } from './user/user.reducer';
import digitalContractReducer from './digitalContract/digitalContract.reducer';
import datasetReducer from './dataset/dataset.reducer';
import accountManagerReducer from './accountManager/accountManager.reducer';
import organizationReducer from './organization/organization.reducer';
import virtualMachineManagerReducer from './virtualMachineManager/virtualMachineManager.reducer';
import azureTemplateReducer from './azureTemplate/azureTemplate.reducer';
import feedReducer from './feed/feed.reducer';
import unifiedRegistryReducer from './unifiedRegistry/unifiedRegistry.reducer';

export interface IState {
  user: IUserState;
  'audit-log-manager': IEventState;
  digitalContract: IDigitalContractState;
  dataset: IDatasetState;
  accountManager: IAccountManagerState;
  organization: IOrganizationState;
  virtualMachineManager: IVirtualMachineState;
  azureTemplate: IAzureTemplateState;
  feed: IFeedState;
  unifiedRegistry: IUnifiedRegistryState;
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
  azureTemplate: azureTemplateReducer,
  feed: feedReducer,
  unifiedRegistry: unifiedRegistryReducer,
});

export default persistReducer(persistConfig, rootReducer);
