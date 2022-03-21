import React from 'react';
import { ConditionalRender } from '@components/ConditionalRender';
import SingleFormViewBG from '@assets/SingleFormViewBG.png';

import { TSignUpProps } from './SignUp.types';

import SignUpForm from './SignUp.form';
import SignUpSuccess from './SignUp.success';
import SignUpFailure from './SignUp.failure';

const SignUp: React.FC<TSignUpProps> = ({
  signUpReset,
  signUpStart,
  userState,
}) => {
  if (userState === 'signup-success') {
    return <SignUpSuccess signUpReset={signUpReset} />;
  }
  return (
    <ConditionalRender
      //@ts-ignore
      state={userState}
      success={() => <></>}
      failure={()=> <SignUpFailure signUpReset={signUpReset}/>}
    >
      <SignUpForm signUpReset={signUpReset} signUpStart={signUpStart} />
    </ConditionalRender>
  );
};

export default SignUp;
