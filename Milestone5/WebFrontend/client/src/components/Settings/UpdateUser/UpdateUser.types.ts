import { TPutUpdateUserStart } from '@redux/accountManager/accountManager.typeDefs';
import { IDefaults } from '@redux/typedefs';
import { IUserData } from '@redux/user/user.typeDefs';

export type TUpdateUserProps = {
  putUpdateUserStart(data: TPutUpdateUserStart): void;
  putUpdateUserReset(): void;
  putUpdateUserState: IDefaults['state'];
  userData: IUserData;
};

export type TUpdateUserFormProps = {
  putUpdateUserStart(data: TPutUpdateUserStart): void;
  putUpdateUserReset(): void;
  userData: IUserData;
};

export type TUpdateUserSuccessProps = {
  putUpdateUserStart(data: TPutUpdateUserStart): void;
  putUpdateUserReset(): void;
  userData: IUserData;
};

export type TUpdateUserFailureProps = {
  putUpdateUserStart(data: TPutUpdateUserStart): void;
  putUpdateUserReset(): void;
  userData: IUserData;
};
