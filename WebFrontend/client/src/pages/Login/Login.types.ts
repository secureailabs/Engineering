import { UseMutateFunction } from 'react-query';
import { AxiosError } from 'axios';
import { IEmailAndPassword } from '@app/redux/user/user.typeDefs';

export type TLoginProps = {
  signInStart: UseMutateFunction<IEmailAndPassword, AxiosError<any>, void, unknown>;
  signInReset(): void;
  status: 'success' | 'error' | 'loading' | 'idle';

};

export type TLoginFormProps = {
  signInStart: UseMutateFunction<IEmailAndPassword, AxiosError<any>, void, unknown>;
  signInReset(): void;
};
