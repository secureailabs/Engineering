import React from 'react';
import { ConditionalRender } from '@components/ConditionalRenderRQuery';

import { TLoginProps } from './Login.types';

import LoginForm from './Login.form';
import LoginSuccess from './Login.success';
import LoginFailure from './Login.failure';
import { AbsoluteSpinner } from '@components/Spinner';

const Login: React.FC<TLoginProps> = ({
  signInReset,
  signInStart,
  status,
}) => {
  return (
    <ConditionalRender
      status={status}
      success={LoginSuccess}
      failure={() => <LoginFailure signInReset={signInReset} />}
      Loading={<AbsoluteSpinner />}
    >
      <LoginForm signInReset={signInReset} signInStart={signInStart} />
    </ConditionalRender>
  );
};

export default Login;
