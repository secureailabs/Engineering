import React from 'react';
import { useHistory } from 'react-router-dom';
import { TSignUpFormProps } from './SignUp.types';
import LoginLinkView from '@components/LoginLinkView';


const SignUp = ({
  signUpReset,
}: {
  signUpReset: TSignUpFormProps['signUpReset'];
}) => {
  const history = useHistory();
  return (
    <>
      <LoginLinkView message="You have successfuly signed up! Please click this link to login."
              onClick={() => {
                signUpReset();
                history.push('/login');
              }}/>
    </>
  );
};

export default SignUp;
