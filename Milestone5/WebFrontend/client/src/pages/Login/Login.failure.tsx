import React from 'react';
import LoginLinkView from '@components/LoginLinkView';
import { TLoginFormProps } from './Login.types';

const LoginFailure = ({
  signInReset,
}: {
  signInReset: TLoginFormProps['signInReset'];
})=> {
  return (
    <LoginLinkView message="There was an error logging you in. Please verify your credentials." onClick={signInReset} />
  );
};

export default LoginFailure;
