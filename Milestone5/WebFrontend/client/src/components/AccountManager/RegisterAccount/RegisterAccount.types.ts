import { TPostAccountManagerStart } from '@redux/accountManager/accountManager.typeDefs';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TRegisterAccountProps = {
  postAccountManagerStart(data: TPostAccountManagerStart): void;
  postAccountManagerReset(): void;
  getAllAccountManagersStart(key: string): void;
  getAllAccountManagersReset(): void;
  postAccountManagerState: IDefaults['state'];
  userData: IUserData;
  closeModal(): void;
};

export type TRegisterAccountFormProps = {
  postAccountManagerStart(data: TPostAccountManagerStart): void;
  postAccountManagerReset(): void;
  userData: IUserData;
};

export type TRegisterAccountSuccess = {
  closeModal(): void;
};
