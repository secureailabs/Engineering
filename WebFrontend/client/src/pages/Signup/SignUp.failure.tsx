import React from 'react';
import LoginLinkView from '@components/LoginLinkView';
import { TSignUpFormProps } from './SignUp.types';


const SignUpFailure = ({
  signUpReset,
}: {
  signUpReset: TSignUpFormProps['signUpReset'];
}) => {
  return <LoginLinkView message="There was an error signing you up. Please try again later" buttonText="Sign Up" onClick={signUpReset} />
};

export default SignUpFailure;
