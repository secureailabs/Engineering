import React from 'react';
import { ConditionalRender } from '@components/ConditionalRender';

import { TLoginProps } from './Login.types';

import LoginForm from './Login.form';
import LoginSuccess from './Login.success';
import LoginFailure from './Login.failure';

const Login: React.FC<TLoginProps> = ({
  signInReset,
  signInStart,
  userState,
}) => {
  return (
    <ConditionalRender
      //@ts-ignore
      state={userState}
      success={LoginSuccess}
      failure={() => <LoginFailure signInReset={signInReset} />}
    >
      <LoginForm signInReset={signInReset} signInStart={signInStart} />
    </ConditionalRender>
  );
};

export default Login;
