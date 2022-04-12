import { TGetAllAccountManagersSuccess } from '@redux/accountManager/accountManager.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TAccountManagerProps = {
  getAllAccountManagersStart(key: string): void;
  getAllAccountManagersReset(): void;
  getAllAccountManagersState: IDefaults['state'];
  getAllAccountManagersData: TGetAllAccountManagersSuccess;
  userData:IUserData;
};

export type TAccountManagerSuccessProps = {
  accountsFilter: string;
  setAccountManagerID(data: string | null): void;
  getAllAccountManagersData: TGetAllAccountManagersSuccess;
};
