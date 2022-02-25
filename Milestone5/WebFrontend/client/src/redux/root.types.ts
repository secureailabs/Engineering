import { userAction } from './user/user.actions';
import { digitalContractActions } from './digitalContract/digitalContract.actions';
import { datasetActions } from './dataset/dataset.actions';
import { AccountManagerActions } from './accountManager/accountManager.actions';
import { OrganizationActions } from './organization/organization.actions';
import { AzureTemplateActions } from './azureTemplate/azureTemplate.actions';
type RootAction =
  | userAction
  | digitalContractActions
  | datasetActions
  | AccountManagerActions
  | OrganizationActions
  | AzureTemplateActions;

export type { RootAction };
