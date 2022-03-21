import { IPostUserStart } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TSignUpProps = {
  signUpStart(data: IPostUserStart): void;
  signUpReset(): void;
  userState: IDefaults['state'] | 'noUserSession' | 'signup-success';
};

export type TSignUpFormProps = {
  signUpStart(data: IPostUserStart): void;
  signUpReset(): void;
};
