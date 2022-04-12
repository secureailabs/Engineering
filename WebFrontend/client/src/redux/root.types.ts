import { userAction } from './user/user.actions';
import { digitalContractActions } from './digitalContract/digitalContract.actions';
import { datasetActions } from './dataset/dataset.actions';
import { AccountManagerActions } from './accountManager/accountManager.actions';
import { OrganizationActions } from './organization/organization.actions';
import { AzureTemplatesManagerActions } from './azureTemplatesManager/azureTemplatesManager.actions';
type RootAction =
  | userAction
  | digitalContractActions
  | datasetActions
  | AccountManagerActions
  | OrganizationActions
  | AzureTemplatesManagerActions

export type { RootAction };
