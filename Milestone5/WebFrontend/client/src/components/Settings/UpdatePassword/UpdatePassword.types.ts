import { TPutUpdatePasswordStart } from '@redux/accountManager/accountManager.typeDefs';
import { IDefaults } from '@redux/typedefs';
import { IUserData } from '@redux/user/user.typeDefs';

export type TUpdatePasswordProps = {
  putUpdatePasswordStart(data: TPutUpdatePasswordStart): void;
  putUpdatePasswordReset(): void;
  putUpdatePasswordState: IDefaults['state'];
  userData: IUserData;
};

export type TUpdatePasswordFormProps = {
  putUpdatePasswordStart(data: TPutUpdatePasswordStart): void;
  putUpdatePasswordReset(): void;
  userData: IUserData;
};

export type TUpdatePasswordSuccessProps = {
  putUpdatePasswordStart(data: TPutUpdatePasswordStart): void;
  putUpdatePasswordReset(): void;
  userData: IUserData;
};

export type TUpdatePasswordFailureProps = {
  putUpdatePasswordStart(data: TPutUpdatePasswordStart): void;
  putUpdatePasswordReset(): void;
  userData: IUserData;
};
