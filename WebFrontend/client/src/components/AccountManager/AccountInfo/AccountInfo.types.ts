import { IDefaults } from '@redux/typedefs';
import { TGetAccountManagerSuccess } from '@redux/accountManager/accountManager.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';

export type TAccountInfoSuccess = {
  getAccountManagerData: TGetAccountManagerSuccess | null;
  accountManagerID: string;
  userData: IUserData;
  slideToPrev(): void;
};

export type TAccountInfo = {
  getAccountManagerData: TGetAccountManagerSuccess | null;
  accountManagerID: string;
  userData: IUserData;
  slideToPrev(): void;
};
