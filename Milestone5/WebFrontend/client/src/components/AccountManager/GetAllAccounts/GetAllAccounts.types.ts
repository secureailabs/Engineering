import { TGetAllAccountManagersSuccess } from '@redux/accountManager/accountManager.typeDefs';

export type TGetAllAccounts = {
  setAccountManagerID(accountManager: string): void;
  data: Array<TGetAllAccountManagersSuccess['OrganizationUsers']['']>;
};