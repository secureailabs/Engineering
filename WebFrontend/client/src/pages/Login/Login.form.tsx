//@ts-nocheck
import React, { useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import login_background from '@assets/login_background.jpg';
import ImageBackground from '@secureailabs/web-ui/components/ImageBackground';
import Form from '@components/Form';
// import FormFieldsRenderer from '@components/FormFieldsRenderer';

import { TLoginFormProps } from './Login.types';
// import LoginScheme from 'src/formSchemes/LoginScheme';
import { IEmailAndPassword } from '@redux/user/user.typeDefs';

import { formData } from './Login.data';

import Button from '@components/Button';

import CardForm from '@secureailabs/web-ui/components/CardForm';
import FormFieldsRenderer from '@secureailabs/web-ui/components/FormFieldsRenderer';
import Margin from '@secureailabs/web-ui/components/Margin';
import Page from '@secureailabs/web-ui/layout/Page';

import SailLogo from '@assets/newLogo.png';

const Login: React.FC<TLoginFormProps> = ({ signInReset, signInStart }) => {
  const { register, handleSubmit, formState, trigger } = useForm({
    // resolver: yupResolver(LoginScheme),
    mode: 'onSubmit',
  });
  useEffect(() => {
    signInReset();
  }, []);
  const onSubmit: SubmitHandler<IEmailAndPassword> = (data) => {
    signInStart(data);
  };
  return (
    <Page pageType="full">
      <ImageBackground image={login_background}>
        <CardForm image={SailLogo}>
          <>
            <form onSubmit={handleSubmit(onSubmit)} className="form">
              <FormFieldsRenderer
                register={register}
                button_text="Login"
                formState={formState}
                fields={{
                  email: {
                    label: 'Email',
                    placeholder: 'Email',
                    type: 'text',
                  },
                  password: {
                    label: 'Password',
                    placeholder: 'Password',
                    type: 'password',
                  },
                }}
              >
                <p
                  style={{
                    width: '100%',
                    textAlign: 'right',
                    marginTop: '-1rem',
                    marginBottom: '2rem',
                  }}
                >
                  <a
                    href="./forgotpassword"
                    style={{
                      width: '100%',
                      fontSize: '1.4rem',
                      fontWeight: 500,
                      lineHeight: '1.7rem',
                      color: 'black',
                      textDecoration: 'None',
                    }}
                  >
                    Forgot Password?
                  </a>
                </p>
              </FormFieldsRenderer>
            </form>
            <Margin size={5} />
            <p
              style={{
                textAlign: 'center',
                fontWeight: 500,
                fontSize: '1.4rem',
                lineHeight: '1.7rem',
              }}
            >
              Don&apos;t have an account?&nbsp;&nbsp;
              <a
                href="./signup"
                style={{
                  color: 'var(--color-primary)',
                  textDecoration: 'None',
                }}
              >
                Signup
              </a>
            </p>
            <Margin size={5} />
          </>
        </CardForm>
      </ImageBackground>
    </Page>
  );
};

export default Login;
