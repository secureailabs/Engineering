import { IEmailAndPassword } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TLoginProps = {
  signInStart(data: IEmailAndPassword): void;
  signInReset(): void;
  userState: IDefaults['state'] | 'noUserSession' | 'signup-success';
};

export type TLoginFormProps = {
  signInStart(data: IEmailAndPassword): void;
  signInReset(): void;
};
