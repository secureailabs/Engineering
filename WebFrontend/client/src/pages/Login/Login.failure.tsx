import React from 'react';
import { TLoginFormProps } from './Login.types';


import Page from '@secureailabs/web-ui/layout/Page';
import ImageBackground from '@secureailabs/web-ui/components/ImageBackground';
import CardForm from '@secureailabs/web-ui/components/CardForm';
import Button from '@secureailabs/web-ui/components/Button';
import Margin from '@secureailabs/web-ui/components/Margin';
import login_background from '@assets/login_background.jpg';
import SailLogo from '@assets/newLogo.png';

const LoginFailure = ({
  signInReset,
}: {
  signInReset: TLoginFormProps['signInReset'];
})=> {
  return (
    <Page pageType="full">
      <ImageBackground image={login_background}>
        <CardForm image={SailLogo}>
          <>
          <p style={{textAlign: 'center', fontSize: '1.25rem'}}>Login has failed. Please check your credentials and/or try again later.</p>
          <Margin size={5} />
          <Button full button_type='primary' onClick={signInReset}>Go Back to Login Page</Button>
          </>
        </CardForm>
      </ImageBackground>
    </Page>
  );
};

export default LoginFailure;
